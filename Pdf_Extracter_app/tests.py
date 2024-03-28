from django.test import TestCase

# Create your tests here.

s = "saregaxxxxxxregasaxxxxxsaregayyyyyysaregayyyyyregama"
l = ["sa","re"]

sa = []
re = []

st = ''
for i in s:
    if i == "x" or i == "y":
        for j in l:
            if j == "sa":
                if st.find(j):
                    sa.append(st)
                    st = '' 

            if j == "re":
                if st.find(j):
                    re.append(st)
                    st = '' 

                   

    else:
        st+=i
print(sa)     










        


