import os

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "index.html")
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

t1 = '<th class="py-3 px-4">Bölgə</th>'
r1 = '<th class="py-3 px-4">Bölgə</th>\n                <th class="py-3 px-4">Məktəb Direktoru</th>'

t2 = '{{ s.region }}</td>'
r2 = '''{{ s.region }}</td>
                <td class="py-3 px-4">
                  <span v-if="s.director_name" class="font-bold text-emerald-800 bg-emerald-100 px-2.5 py-1 rounded-xl text-xs flex items-center gap-1 w-max">
                    <span>🏛️</span>
                    <span>{{ s.director_name }}</span>
                  </span>
                  <span v-else class="text-slate-400 text-xs italic">Təyin olunmayıb</span>
                </td>'''

assert t1 in text, "t1 not found"
assert t2 in text, "t2 not found"

text = text.replace(t1, r1, 1).replace(t2, r2, 1)

with open(path, "w", encoding="utf-8") as f:
    f.write(text)

print("Director column added!")
