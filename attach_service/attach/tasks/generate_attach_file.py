from datetime import datetime
import json
import shutil
from pathlib import Path

import dramatiq

from django.conf import settings

from attach.models import RegistrPeople, GetViewDataAttachPoll


@dramatiq.actor(time_limit=3_600_000)
def generate_attach_file(op_token, date_query):
    print(f'Начало - {datetime.now()}')

    attach_data = RegistrPeople.objects.using("registr").raw(
        '''
        SELECT *
        FROM
        (
        SELECT 
            P.ID, 
            P.ENP AS ENP,
            P.SS,
            P.Q,
            CONVERT(VARCHAR, P.DBEG, 23) AS DBEG,
            A.ID AS HID,
            A.PID,
            A.LPU,
            A.LPUAUTO,
            CONVERT(VARCHAR, A.LPUDT, 23) AS LPUDT,
            CONVERT(VARCHAR, A.LPUDX, 23) AS LPUDX,
            A.LPUTYPE,
            A.OID,
            A.DISTRICT,
            A.SUBDIV,
            A.SS_DOCTOR,
            CONVERT(VARCHAR, P.LPUDT_DOC, 23) AS LPUDT_DOC,
            ROW_NUMBER () OVER ( PARTITION BY A.PID ORDER BY ISNULL(A.LPUDX,'21000101') DESC , A.LPUDT DESC) R
        FROM 
            PEOPLE P
                JOIN HISTLPU A ON P.ID = A.PID
        WHERE 
            P.DBEG <= %s 
            AND ISNULL(P.DSTOP, '21000101') >= %s
            AND A.LPUDT <= %s
            AND ISNULL(A.LPUDX, '21000101') >= %s
        ) T
        WHERE T.R = 1
            ''', 
        [date_query, date_query, date_query, date_query]
    )
    
    attach_list = []
    attach_dict = {}

    for item in attach_data:
        attach_dict["personaEnp"] = item.enp
        if item.ss is not None:
            attach_dict["personaSnils"] = item.ss
        attach_dict["personaPolisBeginD"] = item.dbeg
        attach_dict["personaSmoCode"] = item.q
        attach_dict["attachBeginD"] = item.lpudt
        if item.lpudx is not None:
            attach_dict["attachEndD"] = item.lpudx
        if item.lpuauto is not None:
            attach_dict["attachMethod"] = int(item.lpuauto)
        if item.lputype is not None:
            attach_dict["attachType"] = int(item.lputype)
        if item.DISTRICT is not None:
            attach_dict["areaOID"] = item.DISTRICT
        if item.OID is not None:
            attach_dict["moOID"] = item.OID
        if item.lpu is not None:
            attach_dict["moCode"] = item.lpu
        if item.ss_doctor is not None:
            attach_dict["doctorSnils"] = item.ss_doctor
        if item.lpudt_doc is not None:
            attach_dict["doctorSince"] = item.lpudt_doc
        if item.SUBDIV is not None:
            attach_dict["moDepOID"] = item.SUBDIV
        attach_list.append(attach_dict.copy())
        attach_dict.clear()

    file_path = settings.BASE_DIR / 'temp_files'
    file_json_name = file_path / f'file/{op_token}.json'
    file_zip_name = file_path / f'zip/{op_token}'
    with open(file_json_name, 'w') as f:
        json.dump(attach_list, f, indent=4)

    shutil.make_archive(file_zip_name,'zip',Path(file_json_name).resolve().parent)

    op = GetViewDataAttachPoll.objects.get(op_token=op_token)
    #upload_file = open(file_path / f'{op_token}.zip')
    with open(file_path / f'zip/{op_token}.zip', '+rb') as f:
        op.poll_file.save(f'{op_token}.zip', f)
        op.status = 'COMPLITE'
        op.save()

    Path.unlink(file_json_name)
    Path.unlink(file_path / f'zip/{op_token}.zip')

    print(f'Конец - {datetime.now()}')