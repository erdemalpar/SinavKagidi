import datetime
import os
import re

path = '/Users/erdem/.gemini/antigravity/scratch/sinav-kagidi/templates/soru_bankasi.html'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
marker = f"<!-- Updated at {ts} -->\n"

if "<!-- Updated at" in c:
    # replace existing
    c = re.sub(r"<!-- Updated at .*? -->\n", marker, c)
else:
    # prepend to content block or beginning
    # extends base.html olduğu için bu comment görünmeyebilir renderda ama dosya değişir.
    # en sona ekleyelim block dışına değil.
    # Base layout bozulmasın diye {% block content %} içine ekleyelim.
    if "{% block content %}" in c:
         c = c.replace("{% block content %}", "{% block content %}\n" + marker)
    else:
         c = marker + c

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print(f"Timestamp updated: {ts}")
