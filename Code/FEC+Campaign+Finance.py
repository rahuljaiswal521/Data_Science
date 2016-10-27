
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plot
from matplotlib.ticker import FuncFormatter
from io import StringIO as st
get_ipython().magic('matplotlib inline')


# In[2]:

DATA_DIR='F:\Data_Science\Capstone\FEC Campaign Finance Data'


# In[3]:

CONTRIBUTOR = "{0}/CONTRIBUTOR.csv".format(DATA_DIR)
Expenditure= "{0}/Expenditure.csv".format(DATA_DIR)
Summary= "{0}/report_summaries_form_3p.csv".format(DATA_DIR)


# In[4]:

# test_cont=pd.read_csv(CONTRIBUTOR,index_col=False)


# In[36]:

import matplotlib.dates as dt
dt.num2date(2)


# In[5]:

test_cont=pd.read_csv(CONTRIBUTOR,index_col=False)


# In[6]:

exp=pd.read_csv(Expenditure,index_col=False)


# In[7]:

summ=pd.read_csv(Summary,index_col=False)


# In[8]:

cont_amt=test_cont[['cmte_id','cand_nm','contb_receipt_amt','election_tp']].reset_index(drop=True)


# In[9]:

exp_cmt=pd.DataFrame(cont_amt.groupby(['cmte_id','cand_nm','election_tp'])['contb_receipt_amt'].sum()).reset_index(drop=False)


# In[10]:

exp_cmt.contb_receipt_amt=exp_cmt.contb_receipt_amt.apply(pd.to_numeric)


# In[11]:

exp_cmt=exp_cmt.sort_values('contb_receipt_amt',ascending=False)


# In[12]:

exp_cmt[exp_cmt.election_tp=='P2016'].head(10).plot.barh(x='cand_nm',y='contb_receipt_amt')
plot.xlabel('Amount')
plot.ylabel('Candidate Name')
plot.title('Top 10 Contributon received by Candidates for 2016 Primary Election')
L=plot.legend()
L.get_texts()[0].set_text('Amount')
exp_cmt[exp_cmt.election_tp=='G2016'].head(10).plot.barh(x='cand_nm',y='contb_receipt_amt')
plot.xlabel('Amount')
plot.ylabel('Candidate Name')
plot.title('Top 10 Contributon received by Candidates for 2016 General Election')
L=plot.legend()
L.get_texts()[0].set_text('Amount')


# In[13]:

cont_det=test_cont[['contbr_nm','contbr_city','contb_receipt_amt','election_tp']].reset_index(drop=True)


# In[14]:

cont_by_contbr=cont_det.groupby(['contbr_nm','election_tp'])['contb_receipt_amt'].sum().reset_index(drop=False).sort_values('contb_receipt_amt',ascending=False).reset_index(drop=True)


# In[15]:

cont_by_city=cont_det.groupby(['contbr_city','election_tp'])['contb_receipt_amt'].sum().reset_index(drop=False).sort_values('contb_receipt_amt',ascending=False).reset_index(drop=True)


# In[16]:

cont_by_contbr[cont_by_contbr.election_tp=='P2016'].head(10).plot.barh(x='contbr_nm',y='contb_receipt_amt')
plot.ylabel('Contributer Name')
plot.xlabel('Contributed Money')
plot.title('Money Contributed by top 10 contributer for 2016 Primary Election')
L=plot.legend()
L.get_texts()[0].set_text('Amount')
cont_by_contbr[cont_by_contbr.election_tp=='G2016'].head(10).plot.barh(x='contbr_nm',y='contb_receipt_amt')
plot.ylabel('Contributer Name')
plot.xlabel('Contributed Money')
plot.title('Money Contributed by top 10 contributer for 2016 General Election')
L=plot.legend()
L.get_texts()[0].set_text('Amount')


# In[17]:

cont_by_city.contb_receipt_amt=cont_by_city.contb_receipt_amt.apply(pd.to_numeric)


# In[18]:

cont_by_city[cont_by_city.election_tp=='P2016'].head(10).plot.barh(x='contbr_city',y='contb_receipt_amt')
plot.ylabel('City')
plot.xlabel('Contributed Money')
plot.title('10 Cities contributed most for 2016 Primary Election')
L=plot.legend()
L.get_texts()[0].set_text('Amount')
cont_by_city[cont_by_city.election_tp=='G2016'].head(10).plot.barh(x='contbr_city',y='contb_receipt_amt')
plot.ylabel('City')
plot.xlabel('Contributed Money')
plot.title('10 Cities contributed most for 2016 General Election')
L=plot.legend()
L.get_texts()[0].set_text('Amount')


# In[19]:

exp[['cand_nm','recipient_nm','disb_amt','election_tp']].groupby(['recipient_nm'])['disb_amt'].sum().reset_index(drop=False).sort_values('disb_amt',ascending=False).reset_index(drop=True).head(10).plot.barh(x='recipient_nm',y='disb_amt')

plot.xlabel('Money Received from different Committee')
plot.ylabel('Receiver Name')
plot.title('10 Receipient who got most of the Money')
L=plot.legend()
L.get_texts()[0].set_text('Amount')


exp[['cand_nm','recipient_nm','disb_amt','election_tp']].groupby(['cand_nm'])['disb_amt'].sum().reset_index(drop=False).sort_values('disb_amt',ascending=False).reset_index(drop=True).head(10).plot.barh(x='cand_nm',y='disb_amt')

plot.xlabel('Money Spent By different Candidates')
plot.ylabel('Candidates Name')
plot.title('10 Candidates who spent most Money')
L=plot.legend()
L.get_texts()[0].set_text('Amount')


# In[20]:

exp_cmt[exp_cmt.election_tp=='P2016'].head(5).cmte_id


# In[21]:

a=pd.DataFrame(columns=['recipient_nm','disb_amt','cand_nm'])
ind = np.arange(3) 
x = np.arange(5)
width = 0.35
j=0
x_labels=[1,2,3]
fig, ax = plot.subplots()
for i,row in exp_cmt[exp_cmt.election_tp=='P2016'].head(5).iterrows():
    z=(exp[exp.cmte_id==row.cmte_id].groupby(['recipient_nm'])['disb_amt'].sum().    reset_index(drop=False).sort_values('disb_amt',ascending=False).reset_index(drop=True).head(3))
    z['cand_nm']=row.cand_nm
    a=a.append(z, ignore_index=True)
    a1=ax.barh(ind+j,z.disb_amt,1)
    ax.set_yticklabels((a.cand_nm.drop_duplicates()))
    j=j+4
rects = ax.patches
for rect, label, amt in zip(rects, a.recipient_nm,a.disb_amt):
    height = rect.get_height()
    ax.text(amt,rect.get_y(),  label, ha='left', va='bottom')
plot.xlabel('Money Spent By different Candidates')
plot.ylabel('Candidates Name')
plot.title('Top 3 Recipient by top 5 candidates')
fig.set_size_inches((14,10))
fig.set_dpi(800)


# In[22]:

colums=['CMTE_ID','CMTE_NM','CAND_ID','RPT_YR','RPT_TP','TTL_CONTB_PER','TTL_RECEIPTS_PER']


# In[23]:

cmte_dtls=summ[colums]


# In[25]:

cmte_dtls['month']=(summ.RPT_TP.str.slice(1))


# In[26]:

mydata = [{'Digit' : 1, 'Month':'Jan'},
          {'Digit' : 2, 'Month':'Feb'},
          {'Digit' : 3, 'Month':'Mar'},
          {'Digit' : 4, 'Month':'Apr'},
          {'Digit' : 5, 'Month':'May'},
          {'Digit' : 6, 'Month':'Jun'},
          {'Digit' : 7, 'Month':'Jul'},
          {'Digit' : 8, 'Month':'Aug'},
          {'Digit' : 9, 'Month':'Sep'},
          {'Digit' : 10, 'Month':'Oct'},
          {'Digit' : 11, 'Month':'Nov'},
          {'Digit' : 12, 'Month':'Dec'},
          ]
month = pd.DataFrame(mydata)


# In[27]:

#cmte_dtls.dtypes
cmte_dtls.month=cmte_dtls['month'].convert_objects(convert_numeric=True)


# In[59]:

month.head()


# In[82]:

fig, ax = plot.subplots()
plot.hold(True)
for row in exp_cmt[exp_cmt.election_tp=='P2016'].head(5).cmte_id:
    h=cmte_dtls[(cmte_dtls.CMTE_ID==row)&(cmte_dtls.RPT_TP.str.startswith('M'))].sort_values(['RPT_YR','month'])
    ax.plot((h.month),h.TTL_CONTB_PER,label=cmte_dtls[cmte_dtls.CMTE_ID==row].CMTE_NM.drop_duplicates().values)
ax.set_xticklabels(month.Month+'2016')

fig.set_size_inches((24,10))
fig.set_dpi(800)
ax.grid(True)
ax.legend(loc='best')
ax.xaxis_date
ax.set_ylim(0)
ax.set_ylabel('Money Contributed')
plot.title('Money Contributed to top 5 Committee on each Month')

#ax.xaxis.set_major_locator(cmte_dtls.CAND_ID)


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



