from django.db import models


class RegistrPeople(models.Model):
    fam = models.CharField(db_column='FAM', max_length=40, blank=True, null=True)  # Field name made lowercase.
    im = models.CharField(db_column='IM', max_length=40, blank=True, null=True)  # Field name made lowercase.
    ot = models.CharField(db_column='OT', max_length=40, blank=True, null=True)  # Field name made lowercase.
    w = models.IntegerField(db_column='W', blank=True, null=True)  # Field name made lowercase.
    dost = models.CharField(db_column='DOST', max_length=6, blank=True, null=True)  # Field name made lowercase.
    dr = models.DateTimeField(db_column='DR', blank=True, null=True)  # Field name made lowercase.
    dra = models.BooleanField(db_column='DRA', blank=True, null=True)  # Field name made lowercase.
    drt = models.IntegerField(db_column='DRT', blank=True, null=True)  # Field name made lowercase.
    mr = models.CharField(db_column='MR', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ds = models.DateTimeField(db_column='DS', blank=True, null=True)  # Field name made lowercase.
    ss = models.CharField(db_column='SS', max_length=14, blank=True, null=True)  # Field name made lowercase.
    doctp = models.CharField(db_column='DOCTP', max_length=3, blank=True, null=True)  # Field name made lowercase.
    docs = models.CharField(db_column='DOCS', max_length=20, blank=True, null=True)  # Field name made lowercase.
    docn = models.CharField(db_column='DOCN', max_length=20, blank=True, null=True)  # Field name made lowercase.
    docdt = models.DateTimeField(db_column='DOCDT', blank=True, null=True)  # Field name made lowercase.
    docorg = models.CharField(db_column='DOCORG', max_length=255, blank=True, null=True)  # Field name made lowercase.
    docend = models.DateTimeField(db_column='DOCEND', blank=True, null=True)  # Field name made lowercase.
    rdoctp = models.CharField(db_column='RDOCTP', max_length=3, blank=True, null=True)  # Field name made lowercase.
    rdocs = models.CharField(db_column='RDOCS', max_length=20, blank=True, null=True)  # Field name made lowercase.
    rdocn = models.CharField(db_column='RDOCN', max_length=20, blank=True, null=True)  # Field name made lowercase.
    rdocdt = models.DateTimeField(db_column='RDOCDT', blank=True, null=True)  # Field name made lowercase.
    rdocorg = models.CharField(db_column='RDOCORG', max_length=255, blank=True, null=True)  # Field name made lowercase.
    rdocend = models.DateTimeField(db_column='RDOCEND', blank=True, null=True)  # Field name made lowercase.
    birth_oksm = models.CharField(db_column='BIRTH_OKSM', max_length=3, blank=True, null=True)  # Field name made lowercase.
    cn = models.CharField(db_column='CN', max_length=3, blank=True, null=True)  # Field name made lowercase.
    subj = models.CharField(db_column='SUBJ', max_length=5, blank=True, null=True)  # Field name made lowercase.
    rn = models.CharField(db_column='RN', max_length=11, blank=True, null=True)  # Field name made lowercase.
    indx = models.CharField(db_column='INDX', max_length=6, blank=True, null=True)  # Field name made lowercase.
    rnname = models.CharField(db_column='RNNAME', max_length=120, blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(db_column='CITY', max_length=120, blank=True, null=True)  # Field name made lowercase.
    np = models.CharField(db_column='NP', max_length=120, blank=True, null=True)  # Field name made lowercase.
    ul = models.CharField(db_column='UL', max_length=120, blank=True, null=True)  # Field name made lowercase.
    dom = models.CharField(db_column='DOM', max_length=20, blank=True, null=True)  # Field name made lowercase.
    kor = models.CharField(db_column='KOR', max_length=12, blank=True, null=True)  # Field name made lowercase.
    kv = models.CharField(db_column='KV', max_length=12, blank=True, null=True)  # Field name made lowercase.
    dmj = models.DateTimeField(db_column='DMJ', blank=True, null=True)  # Field name made lowercase.
    bomj = models.BooleanField(db_column='BOMJ', blank=True, null=True)  # Field name made lowercase.
    kateg = models.IntegerField(db_column='KATEG', blank=True, null=True)  # Field name made lowercase.
    psubj = models.CharField(db_column='PSUBJ', max_length=5, blank=True, null=True)  # Field name made lowercase.
    prn = models.CharField(db_column='PRN', max_length=11, blank=True, null=True)  # Field name made lowercase.
    pindx = models.CharField(db_column='PINDX', max_length=6, blank=True, null=True)  # Field name made lowercase.
    prnname = models.CharField(db_column='PRNNAME', max_length=120, blank=True, null=True)  # Field name made lowercase.
    pcity = models.CharField(db_column='PCITY', max_length=120, blank=True, null=True)  # Field name made lowercase.
    pnp = models.CharField(db_column='PNP', max_length=120, blank=True, null=True)  # Field name made lowercase.
    pul = models.CharField(db_column='PUL', max_length=120, blank=True, null=True)  # Field name made lowercase.
    pdom = models.CharField(db_column='PDOM', max_length=20, blank=True, null=True)  # Field name made lowercase.
    pkor = models.CharField(db_column='PKOR', max_length=12, blank=True, null=True)  # Field name made lowercase.
    pkv = models.CharField(db_column='PKV', max_length=12, blank=True, null=True)  # Field name made lowercase.
    pdmj = models.DateTimeField(db_column='PDMJ', blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='EMAIL', max_length=50, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='PHONE', max_length=40, blank=True, null=True)  # Field name made lowercase.
    enp = models.CharField(db_column='ENP', max_length=16, blank=True, null=True)  # Field name made lowercase.
    q = models.CharField(db_column='Q', max_length=5, blank=True, null=True)  # Field name made lowercase.
    qogrn = models.CharField(db_column='QOGRN', max_length=15, blank=True, null=True)  # Field name made lowercase.
    prz = models.CharField(db_column='PRZ', max_length=8, blank=True, null=True)  # Field name made lowercase.
    opdoc = models.IntegerField(db_column='OPDOC', blank=True, null=True)  # Field name made lowercase.
    spol = models.CharField(db_column='SPOL', max_length=20, blank=True, null=True)  # Field name made lowercase.
    npol = models.CharField(db_column='NPOL', max_length=20, blank=True, null=True)  # Field name made lowercase.
    okato = models.CharField(db_column='OKATO', max_length=5, blank=True, null=True)  # Field name made lowercase.
    dhpol = models.DateTimeField(db_column='DHPOL', blank=True, null=True)  # Field name made lowercase.
    dbeg = models.DateTimeField(db_column='DBEG', blank=True, null=True)  # Field name made lowercase.
    dend = models.DateTimeField(db_column='DEND', blank=True, null=True)  # Field name made lowercase.
    dstop = models.DateTimeField(db_column='DSTOP', blank=True, null=True)  # Field name made lowercase.
    dstop_cs = models.DateTimeField(db_column='DSTOP_CS', blank=True, null=True)  # Field name made lowercase.
    dviz = models.DateTimeField(db_column='DVIZ', blank=True, null=True)  # Field name made lowercase.
    dz = models.DateTimeField(db_column='DZ', blank=True, null=True)  # Field name made lowercase.
    meth = models.IntegerField(db_column='METH', blank=True, null=True)  # Field name made lowercase.
    polisid = models.IntegerField(db_column='POLISID', blank=True, null=True)  # Field name made lowercase.
    rstop = models.IntegerField(db_column='RSTOP', blank=True, null=True)  # Field name made lowercase.
    lpu = models.CharField(db_column='LPU', max_length=15, blank=True, null=True)  # Field name made lowercase.
    lpuwk = models.CharField(db_column='LPUWK', max_length=15, blank=True, null=True)  # Field name made lowercase.
    lpust = models.CharField(db_column='LPUST', max_length=15, blank=True, null=True)  # Field name made lowercase.
    lpuuch = models.CharField(db_column='LPUUCH', max_length=64, blank=True, null=True)  # Field name made lowercase.
    lpuauto = models.IntegerField(db_column='LPUAUTO', blank=True, null=True)  # Field name made lowercase.
    lpudt = models.DateTimeField(db_column='LPUDT', blank=True, null=True)  # Field name made lowercase.
    lpudx = models.DateTimeField(db_column='LPUDX', blank=True, null=True)  # Field name made lowercase.
    sp = models.CharField(db_column='SP', max_length=2, blank=True, null=True)  # Field name made lowercase.
    kt = models.CharField(db_column='KT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    okved = models.CharField(db_column='OKVED', max_length=10, blank=True, null=True)  # Field name made lowercase.
    kladrs = models.CharField(db_column='KLADRS', max_length=15, blank=True, null=True)  # Field name made lowercase.
    erp = models.BooleanField(db_column='ERP', blank=True, null=True)  # Field name made lowercase.
    petition = models.BooleanField(db_column='PETITION', blank=True, null=True)  # Field name made lowercase.
    fiopr = models.CharField(db_column='FIOPR', max_length=200, blank=True, null=True)  # Field name made lowercase.
    contact = models.CharField(db_column='CONTACT', max_length=200, blank=True, null=True)  # Field name made lowercase.
    zfam = models.CharField(db_column='ZFAM', max_length=40, blank=True, null=True)  # Field name made lowercase.
    zim = models.CharField(db_column='ZIM', max_length=40, blank=True, null=True)  # Field name made lowercase.
    zot = models.CharField(db_column='ZOT', max_length=40, blank=True, null=True)  # Field name made lowercase.
    zt = models.IntegerField(db_column='ZT', blank=True, null=True)  # Field name made lowercase.
    zdr = models.DateTimeField(db_column='ZDR', blank=True, null=True)  # Field name made lowercase.
    zmr = models.CharField(db_column='ZMR', max_length=100, blank=True, null=True)  # Field name made lowercase.
    zdoctp = models.CharField(db_column='ZDOCTP', max_length=3, blank=True, null=True)  # Field name made lowercase.
    zdocs = models.CharField(db_column='ZDOCS', max_length=20, blank=True, null=True)  # Field name made lowercase.
    zdocn = models.CharField(db_column='ZDOCN', max_length=20, blank=True, null=True)  # Field name made lowercase.
    zdocdt = models.DateTimeField(db_column='ZDOCDT', blank=True, null=True)  # Field name made lowercase.
    zdocorg = models.CharField(db_column='ZDOCORG', max_length=255, blank=True, null=True)  # Field name made lowercase.
    zaddr = models.CharField(db_column='ZADDR', max_length=255, blank=True, null=True)  # Field name made lowercase.
    zphone = models.CharField(db_column='ZPHONE', max_length=40, blank=True, null=True)  # Field name made lowercase.
    photo = models.TextField(db_column='PHOTO', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    signat = models.TextField(db_column='SIGNAT', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    ptype = models.CharField(db_column='PTYPE', max_length=4, blank=True, null=True)  # Field name made lowercase.
    nord = models.CharField(db_column='NORD', max_length=100, blank=True, null=True)  # Field name made lowercase.
    dord = models.DateTimeField(db_column='DORD', blank=True, null=True)  # Field name made lowercase.
    oldenp = models.CharField(db_column='OLDENP', max_length=16, blank=True, null=True)  # Field name made lowercase.
    kladrg = models.CharField(db_column='KLADRG', max_length=19, blank=True, null=True)  # Field name made lowercase.
    kladrp = models.CharField(db_column='KLADRP', max_length=19, blank=True, null=True)  # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    pid = models.IntegerField(db_column='PID', blank=True, null=True)  # Field name made lowercase.
    #zid = models.ForeignKey('Zajavka', models.DO_NOTHING, db_column='ZID', blank=True, null=True)  # Field name made lowercase.
    bid = models.IntegerField(db_column='BID', blank=True, null=True)  # Field name made lowercase.
    mid = models.IntegerField(db_column='MID', blank=True, null=True)  # Field name made lowercase.
    dedit = models.DateTimeField(db_column='DEDIT', blank=True, null=True)  # Field name made lowercase.
    derp = models.DateTimeField(db_column='DERP', blank=True, null=True)  # Field name made lowercase.
    unemp = models.BooleanField(db_column='UNEMP', blank=True, null=True)  # Field name made lowercase.
    other = models.BooleanField(db_column='OTHER', blank=True, null=True)  # Field name made lowercase.
    dakt = models.DateTimeField(db_column='DAKT', blank=True, null=True)  # Field name made lowercase.
    nakt = models.CharField(db_column='NAKT', max_length=20, blank=True, null=True)  # Field name made lowercase.
    takt = models.CharField(db_column='TAKT', max_length=11, blank=True, null=True)  # Field name made lowercase.
    zenp = models.CharField(db_column='ZENP', max_length=15, blank=True, null=True)  # Field name made lowercase.
    denp = models.DateTimeField(db_column='DENP', blank=True, null=True)  # Field name made lowercase.
    zerr = models.CharField(db_column='ZERR', max_length=40, blank=True, null=True)  # Field name made lowercase.
    dzp1 = models.DateTimeField(db_column='DZP1', blank=True, null=True)  # Field name made lowercase.
    zp1repl = models.CharField(db_column='ZP1REPL', max_length=250, blank=True, null=True)  # Field name made lowercase.
    extid = models.CharField(db_column='EXTID', max_length=36, blank=True, null=True)  # Field name made lowercase.
    fame = models.CharField(db_column='FAME', max_length=40, blank=True, null=True)  # Field name made lowercase.
    ime = models.CharField(db_column='IME', max_length=40, blank=True, null=True)  # Field name made lowercase.
    ote = models.CharField(db_column='OTE', max_length=40, blank=True, null=True)  # Field name made lowercase.
    ssold = models.CharField(db_column='SSOLD', max_length=14, blank=True, null=True)  # Field name made lowercase.
    opsmo = models.IntegerField(db_column='OPSMO', blank=True, null=True)  # Field name made lowercase.
    oppol = models.IntegerField(db_column='OPPOL', blank=True, null=True)  # Field name made lowercase.
    polpr = models.IntegerField(db_column='POLPR', blank=True, null=True)  # Field name made lowercase.
    polvid = models.IntegerField(db_column='POLVID', blank=True, null=True)  # Field name made lowercase.
    pfrss = models.CharField(db_column='PFRSS', max_length=14, blank=True, null=True)  # Field name made lowercase.
    del_field = models.BooleanField(db_column='DEL', blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
    tenp = models.IntegerField(db_column='TENP', blank=True, null=True)  # Field name made lowercase.
    senp = models.CharField(db_column='SENP', max_length=16, blank=True, null=True)  # Field name made lowercase.
    force = models.IntegerField(db_column='FORCE', blank=True, null=True)  # Field name made lowercase.
    pz_scan = models.BooleanField(db_column='PZ_SCAN', blank=True, null=True)  # Field name made lowercase.
    isexported = models.BooleanField(db_column='ISEXPORTED', blank=True, null=True)  # Field name made lowercase.
    exporterror = models.CharField(db_column='EXPORTERROR', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='REMARK', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    fias_aoid = models.CharField(db_column='FIAS_AOID', max_length=36, blank=True, null=True)  # Field name made lowercase.
    fias_houseid = models.CharField(db_column='FIAS_HOUSEID', max_length=36, blank=True, null=True)  # Field name made lowercase.
    pfias_aoid = models.CharField(db_column='PFIAS_AOID', max_length=36, blank=True, null=True)  # Field name made lowercase.
    pfias_houseid = models.CharField(db_column='PFIAS_HOUSEID', max_length=36, blank=True, null=True)  # Field name made lowercase.
    lpuerr = models.CharField(db_column='LPUERR', max_length=30, blank=True, null=True)  # Field name made lowercase.
    lpudsend = models.DateTimeField(db_column='LPUDSEND', blank=True, null=True)  # Field name made lowercase.
    lpudt_doc = models.DateTimeField(db_column='LPUDT_DOC', blank=True, null=True)  # Field name made lowercase.
    lpudt_fel = models.DateTimeField(db_column='LPUDT_FEL', blank=True, null=True)  # Field name made lowercase.
    ss_doctor = models.CharField(db_column='SS_DOCTOR', max_length=11, blank=True, null=True)  # Field name made lowercase.
    ss_feldsher = models.CharField(db_column='SS_FELDSHER', max_length=11, blank=True, null=True)  # Field name made lowercase.
    lpu_conf = models.BooleanField(db_column='LPU_CONF', blank=True, null=True)  # Field name made lowercase.
    err_m = models.CharField(db_column='ERR_M', max_length=20, blank=True, null=True)  # Field name made lowercase.
    err_g = models.CharField(db_column='ERR_G', max_length=20, blank=True, null=True)  # Field name made lowercase.
    lputype = models.CharField(db_column='LPUTYPE', max_length=3, blank=True, null=True)  # Field name made lowercase.
    fias_aoguid = models.CharField(db_column='FIAS_AOGUID', max_length=36, blank=True, null=True)  # Field name made lowercase.
    fias_houseguid = models.CharField(db_column='FIAS_HOUSEGUID', max_length=36, blank=True, null=True)  # Field name made lowercase.
    pfias_aoguid = models.CharField(db_column='PFIAS_AOGUID', max_length=36, blank=True, null=True)  # Field name made lowercase.
    pfias_houseguid = models.CharField(db_column='PFIAS_HOUSEGUID', max_length=36, blank=True, null=True)  # Field name made lowercase.
    lpustdt = models.DateTimeField(db_column='LPUSTDT', blank=True, null=True)  # Field name made lowercase.
    lpustdx = models.DateTimeField(db_column='LPUSTDX', blank=True, null=True)  # Field name made lowercase.
    lpusttype = models.CharField(db_column='LPUSTTYPE', max_length=3, blank=True, null=True)  # Field name made lowercase.
    prik_subj_dr = models.CharField(db_column='PRIK_SUBJ_DR', max_length=5, blank=True, null=True)  # Field name made lowercase.
    lpu_dr = models.CharField(db_column='LPU_DR', max_length=15, blank=True, null=True)  # Field name made lowercase.
    lpudt_dr = models.DateTimeField(db_column='LPUDT_DR', blank=True, null=True)  # Field name made lowercase.
    ss_doctor_dr = models.CharField(db_column='SS_DOCTOR_DR', max_length=11, blank=True, null=True)  # Field name made lowercase.
    lpudt_doc_dr = models.DateTimeField(db_column='LPUDT_DOC_DR', blank=True, null=True)  # Field name made lowercase.
    vs_form = models.IntegerField(db_column='VS_FORM', blank=True, null=True)  # Field name made lowercase.
    truess = models.BooleanField(db_column='TRUESS', blank=True, null=True)  # Field name made lowercase.
    mvdvalid = models.IntegerField(db_column='MVDVALID', blank=True, null=True)  # Field name made lowercase.
    mvdinvalidreason = models.CharField(db_column='MVDINVALIDREASON', max_length=100, blank=True, null=True)  # Field name made lowercase.
    lpu_sp1 = models.CharField(db_column='LPU_SP1', max_length=20, blank=True, null=True)  # Field name made lowercase.
    lpudt1 = models.DateTimeField(db_column='LPUDT1', blank=True, null=True)  # Field name made lowercase.
    lpudx1 = models.DateTimeField(db_column='LPUDX1', blank=True, null=True)  # Field name made lowercase.
    lpuauto1 = models.IntegerField(db_column='LPUAUTO1', blank=True, null=True)  # Field name made lowercase.
    lpu_sp2 = models.CharField(db_column='LPU_SP2', max_length=20, blank=True, null=True)  # Field name made lowercase.
    lpudt2 = models.DateTimeField(db_column='LPUDT2', blank=True, null=True)  # Field name made lowercase.
    lpudx2 = models.DateTimeField(db_column='LPUDX2', blank=True, null=True)  # Field name made lowercase.
    lpuauto2 = models.IntegerField(db_column='LPUAUTO2', blank=True, null=True)  # Field name made lowercase.
    lpu_sp3 = models.CharField(db_column='LPU_SP3', max_length=20, blank=True, null=True)  # Field name made lowercase.
    lpudt3 = models.DateTimeField(db_column='LPUDT3', blank=True, null=True)  # Field name made lowercase.
    lpudx3 = models.DateTimeField(db_column='LPUDX3', blank=True, null=True)  # Field name made lowercase.
    lpuauto3 = models.IntegerField(db_column='LPUAUTO3', blank=True, null=True)  # Field name made lowercase.
    oip = models.CharField(db_column='OIP', max_length=36, blank=True, null=True)  # Field name made lowercase.
    doc_oksm = models.CharField(db_column='DOC_OKSM', max_length=3, blank=True, null=True)  # Field name made lowercase.
    docorgcode = models.CharField(db_column='DOCORGCODE', max_length=7, blank=True, null=True)  # Field name made lowercase.
    rdoccn = models.CharField(db_column='RDOCCN', max_length=3, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'PEOPLE'


class RegistrHistlpu(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    pid = models.ForeignKey(RegistrPeople, related_name='attach', db_column='PID', on_delete=models.DO_NOTHING)  # Field name made lowercase.
    dedit = models.DateTimeField(db_column='DEDIT', blank=True, null=True)  # Field name made lowercase.
    lpu = models.CharField(db_column='LPU', max_length=15, blank=True, null=True)  # Field name made lowercase.
    lpuauto = models.IntegerField(db_column='LPUAUTO', blank=True, null=True)  # Field name made lowercase.
    lpudt = models.DateTimeField(db_column='LPUDT', blank=True, null=True)  # Field name made lowercase.
    lpudx = models.DateTimeField(db_column='LPUDX', blank=True, null=True)  # Field name made lowercase.
    lputype = models.CharField(db_column='LPUTYPE', max_length=3, blank=True, null=True)  # Field name made lowercase.
    lpu_conf = models.BooleanField(db_column='LPU_CONF', blank=True, null=True)  # Field name made lowercase.
    oid = models.CharField(db_column='OID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    district = models.CharField(db_column='DISTRICT', max_length=64, blank=True, null=True)  # Field name made lowercase.
    subdiv = models.CharField(db_column='SUBDIV', max_length=64, blank=True, null=True)  # Field name made lowercase.
    ss_doctor = models.CharField(db_column='SS_DOCTOR', max_length=11, blank=True, null=True)  # Field name made lowercase.
    kateg = models.IntegerField(db_column='KATEG', blank=True, null=True)  # Field name made lowercase.
    op = models.CharField(db_column='OP', max_length=1, blank=True, null=True)  # Field name made lowercase.
    dsend = models.DateTimeField(db_column='DSEND', blank=True, null=True)  # Field name made lowercase.
    dsend_mo = models.DateTimeField(db_column='DSEND_MO', blank=True, null=True)  # Field name made lowercase.
    rclose = models.IntegerField(db_column='RCLOSE', blank=True, null=True)  # Field name made lowercase.
    recin = models.IntegerField(db_column='RECIN', blank=True, null=True)  # Field name made lowercase.
    fileout = models.IntegerField(db_column='FILEOUT', blank=True, null=True)  # Field name made lowercase.
    err_cs = models.CharField(db_column='ERR_CS', max_length=30, blank=True, null=True)  # Field name made lowercase.
    idtfoms = models.IntegerField(db_column='IDTFOMS', blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='REMARK', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'HISTLPU'


class RegistrPolis(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    pid = models.ForeignKey(RegistrPeople, related_name='polis', db_column='PID', on_delete=models.DO_NOTHING)  # Field name made lowercase.
    dedit = models.DateTimeField(db_column='DEDIT', blank=True, null=True)  # Field name made lowercase.
    q = models.CharField(db_column='Q', max_length=5, blank=True, null=True)  # Field name made lowercase.
    qogrn = models.CharField(db_column='QOGRN', max_length=15, blank=True, null=True)  # Field name made lowercase.
    prz = models.CharField(db_column='PRZ', max_length=8, blank=True, null=True)  # Field name made lowercase.
    spol = models.CharField(db_column='SPOL', max_length=20, blank=True, null=True)  # Field name made lowercase.
    npol = models.CharField(db_column='NPOL', max_length=20, blank=True, null=True)  # Field name made lowercase.
    poltp = models.IntegerField(db_column='POLTP', blank=True, null=True)  # Field name made lowercase.
    polvid = models.IntegerField(db_column='POLVID', blank=True, null=True)  # Field name made lowercase.
    dbeg = models.DateTimeField(db_column='DBEG', blank=True, null=True)  # Field name made lowercase.
    dend = models.DateTimeField(db_column='DEND', blank=True, null=True)  # Field name made lowercase.
    rstop = models.IntegerField(db_column='RSTOP', blank=True, null=True)  # Field name made lowercase.
    dstop = models.DateTimeField(db_column='DSTOP', blank=True, null=True)  # Field name made lowercase.
    dstop_cs = models.DateTimeField(db_column='DSTOP_CS', blank=True, null=True)  # Field name made lowercase.
    st = models.IntegerField(db_column='ST', blank=True, null=True)  # Field name made lowercase.
    del_field = models.BooleanField(db_column='DEL', blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
    okato = models.CharField(db_column='OKATO', max_length=11, blank=True, null=True)  # Field name made lowercase.
    nvs = models.CharField(db_column='NVS', max_length=9, blank=True, null=True)  # Field name made lowercase.
    dvs = models.DateTimeField(db_column='DVS', blank=True, null=True)  # Field name made lowercase.
    et = models.DateTimeField(db_column='ET', blank=True, null=True)  # Field name made lowercase.
    unload = models.DateTimeField(db_column='UNLOAD', blank=True, null=True)  # Field name made lowercase.
    dz = models.DateTimeField(db_column='DZ', blank=True, null=True)  # Field name made lowercase.
    dp = models.DateTimeField(db_column='DP', blank=True, null=True)  # Field name made lowercase.
    dh = models.DateTimeField(db_column='DH', blank=True, null=True)  # Field name made lowercase.
    err = models.CharField(db_column='ERR', max_length=200, blank=True, null=True)  # Field name made lowercase.
    oldpid = models.IntegerField(db_column='OLDPID', blank=True, null=True)  # Field name made lowercase.
    sout = models.DateTimeField(db_column='SOUT', blank=True, null=True)  # Field name made lowercase.
    m2id = models.IntegerField(db_column='M2ID', blank=True, null=True)  # Field name made lowercase.
    vs_form = models.IntegerField(db_column='VS_FORM', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'POLIS'