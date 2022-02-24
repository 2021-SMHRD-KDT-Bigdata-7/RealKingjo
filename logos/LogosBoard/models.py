from django.db import models

# Create your models here.


class TAd(models.Model):
    ad_seq = models.AutoField(primary_key=True)
    ad_prenum = models.CharField(max_length=200)
    ad_content = models.TextField()
    ad_subj = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 't_ad'


class TCivil(models.Model):
    civ_seq = models.AutoField(primary_key=True)
    civ_prenum = models.CharField(max_length=200)
    civ_content = models.TextField()
    civ_subj = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 't_civil'


class TCriminal(models.Model):
    cri_seq = models.AutoField(primary_key=True)
    cri_prenum = models.CharField(max_length=200)
    cri_content = models.TextField()
    cri_subj = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 't_criminal'


class TFamily(models.Model):
    fam_seq = models.AutoField(primary_key=True)
    fam_prenum = models.CharField(max_length=200, blank=True, null=True)
    fam_subj = models.CharField(max_length=200, blank=True, null=True)
    fam_content = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_family'


class TLaw(models.Model):
    law_type = models.IntegerField(blank=True, null=True)
    lawc_name = models.TextField(db_column='lawC_name', blank=True, null=True)  # Field name made lowercase.
    law_content = models.TextField(blank=True, null=True)
    m_id = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_law'


class TLog(models.Model):
    log_seq = models.AutoField(primary_key=True)
    log_key = models.CharField(max_length=200)
    log_full = models.TextField()
    log_time = models.DateTimeField()
    log_status = models.CharField(max_length=1)
    id = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 't_log'

class STOPWORD(models.Model):
    word_seq = models.AutoField(primary_key=True)
    word_content= models.CharField(max_length=200)
    
class SYNONYM(models.Model):
    syn_seq = models.AutoField(primary_key=True)
    syn_content=models.CharField(max_length=200)
    
class TCriminalSummary(models.Model):
    cri_seq = models.OneToOneField(TCriminal, models.DO_NOTHING, db_column='cri_seq', primary_key=True)
    cri_subj = models.CharField(max_length=200)
    cri_sum_content = models.TextField()
    cri_sum_keyword = models.CharField(max_length=200, blank=True, null=True)
    cri_sum_abst = models.TextField()
    ref_law = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_criminal_summary'
