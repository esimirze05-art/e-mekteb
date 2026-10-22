import os

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "index.html")
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Global replace E.məktəb -> E-məktəb
text = text.replace("E.məktəb", "E-məktəb")

# 2. In sId definitions, include currentUser.role === 'director'
text = text.replace(
    "const sId = this.currentUser && this.currentUser.is_moderator ? this.currentUser.school_id : this.selectedAdminSchoolId;",
    "const sId = this.currentUser && (this.currentUser.role === 'director' || this.currentUser.is_moderator) ? this.currentUser.school_id : this.selectedAdminSchoolId;"
)

text = text.replace(
    "const sId = this.currentUser && this.currentUser.is_moderator ? this.currentUser.school_id : (this.selectedAdminSchoolId || 1);",
    "const sId = this.currentUser && (this.currentUser.role === 'director' || this.currentUser.is_moderator) ? this.currentUser.school_id : (this.selectedAdminSchoolId || 1);"
)

# 3. Add batch promote card and single class promote button in adminTab === 'classes'
old_classes_hdr = '''      <!-- TAB 4: SİNİFLƏRİN VƏ İNDEKSLƏRİN İDARƏ EDİLMƏSİ (ARTIR / AZALT) -->
      <div v-if="adminTab === 'classes'" class="space-y-6">
        <div>
          <h3 class="text-base font-black text-slate-900">🏫 Siniflər və İndekslərin İdarəsi (Cəmi {{ allClasses.length }} sinif)</h3>
          <p class="text-xs text-slate-500">Hər pillə üzrə indeksləri (A, B, C, D...) artıra və ya azalda (silə) bilərsiniz.</p>
        </div>'''

new_classes_hdr = '''      <!-- TAB 4: SİNİFLƏRİN VƏ İNDEKSLƏRİN İDARƏ EDİLMƏSİ (ARTIR / AZALT) -->
      <div v-if="adminTab === 'classes'" class="space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <h3 class="text-base font-black text-slate-900">🏫 Siniflər və İndekslərin İdarəsi (Cəmi {{ allClasses.length }} sinif)</h3>
            <p class="text-xs text-slate-500">
              {{ currentUser.role === 'director' ? currentUser.school_name + ' üzrə siniflər və indekslər' : 'Sinifləri artırın, azaldın və ya növbəti tədris ilinə keçirin.' }}
            </p>
          </div>
        </div>

        <!-- Avtomatik Sinif Artırma (Növbəti Tədris İlinə Keçid) Banneri -->
        <div class="bg-gradient-to-r from-blue-700 via-indigo-700 to-purple-800 rounded-3xl p-5 text-white shadow-lg flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div class="space-y-1">
            <div class="inline-flex items-center gap-1.5 bg-white/20 px-2.5 py-0.5 rounded-full text-[11px] font-bold">
              <span>⚡ Avtomatik Keçid</span>
            </div>
            <h4 class="text-base font-black">Növbəti Tədris İlinə Keçid (Sinifləri 1 İl Artır)</h4>
            <p class="text-xs text-blue-100 leading-relaxed max-w-xl">
              Məktəbdəki bütün siniflər avtomatik növbəti sinfə yüksəlir (məs. <strong>1A ➔ 2A, 5B ➔ 6B</strong>). İndekslər eyni qalır. Şagirdlər avtomatik yeni sinfə keçir və 11-ci siniflər məzun olur!
            </p>
          </div>
          <button @click="promoteAllClassesInSchool" 
                  class="touch-btn px-5 py-3 bg-white hover:bg-blue-50 text-brand-800 font-black rounded-2xl text-xs shadow-xl shrink-0 flex items-center gap-2">
            <span>🔄 Bütün Sinifləri 1 İl Artır</span>
          </button>
        </div>'''

assert old_classes_hdr in text, "old_classes_hdr not found"
text = text.replace(old_classes_hdr, new_classes_hdr, 1)

# Add single-class promote button on each class badge
old_class_badge = '''              <div v-for="c in getClassesByGrade(gr)" :key="c.id" 
                   class="inline-flex items-center gap-2 bg-slate-50 hover:bg-brand-50 border border-slate-200 hover:border-brand-300 rounded-2xl py-1.5 px-3 transition-all group">
                <span class="text-base font-black text-brand-700">{{ c.name }}</span>
                <span class="text-[10px] font-semibold text-slate-400">({{ c.student_count }} şagird)</span>
                <button @click="adminDeleteClass(c)" title="Bu sinfi sil (azalt)" 
                        class="w-5 h-5 rounded-full bg-slate-200 hover:bg-rose-500 hover:text-white flex items-center justify-center text-xs font-bold text-slate-500 transition-colors ml-1">
                  ✕
                </button>
              </div>'''

new_class_badge = '''              <div v-for="c in getClassesByGrade(gr)" :key="c.id" 
                   class="inline-flex items-center gap-2 bg-white hover:bg-brand-50 border-2 border-slate-200 hover:border-brand-400 rounded-2xl py-1.5 px-3 transition-all shadow-sm group">
                <span class="text-base font-black text-brand-700">{{ c.name }}</span>
                <span class="text-[10px] font-semibold text-slate-500">({{ c.student_count }} şagird)</span>
                
                <!-- 1 Sinif Artır (İndeks eyni qalır) -->
                <button @click="promoteSingleClass(c)" title="Bu sinfi 1 pillə artır (məs. 5B ➔ 6B)" 
                        class="px-2 py-0.5 rounded-lg bg-emerald-100 hover:bg-emerald-200 text-emerald-800 text-[11px] font-black flex items-center gap-0.5 transition-colors">
                  <span>⬆ +1 İl</span>
                </button>

                <!-- Sinfi Sil (Azalt) -->
                <button @click="adminDeleteClass(c)" title="Bu sinfi sil (azalt)" 
                        class="w-5 h-5 rounded-full bg-slate-100 hover:bg-rose-500 hover:text-white flex items-center justify-center text-xs font-bold text-slate-500 transition-colors ml-1">
                  ✕
                </button>
              </div>'''

assert old_class_badge in text, "old_class_badge not found"
text = text.replace(old_class_badge, new_class_badge, 1)

# Add Vue methods: promoteSingleClass and promoteAllClassesInSchool
old_methods_anchor = '''      async adminQuickAddIndex(grade) {'''

new_methods = '''      async promoteSingleClass(c) {
        if (!confirm(`"${c.name}" sinfini 1 pillə artırmaq istəyirsiniz?\\n(İndeks "${c.section}" eyni qalacaq, şagirdlər avtomatik növbəti sinfə keçəcək)`)) return;
        try {
          const res = await fetch(`/api/admin/classes/${c.id}/promote`, { method: 'POST' });
          const d = await res.json();
          if (res.ok) {
            this.showToast(d.message);
            await this.loadAllClasses();
            await this.loadAdminOverview();
          } else {
            this.showToast(d.detail || 'Xəta baş verdi', 'error');
          }
        } catch(e) {
          this.showToast('Xəta baş verdi', 'error');
        }
      },

      async promoteAllClassesInSchool() {
        const sId = this.currentUser && (this.currentUser.role === 'director' || this.currentUser.is_moderator) 
                    ? this.currentUser.school_id 
                    : (this.selectedAdminSchoolId || 1);
        if (!confirm('DİQQƏT: Bu məktəbdəki BÜTÜN sinifləri 1 il artırmaq istəyirsiniz?\\n\\n- Bütün siniflərin indeksi eyni qalacaq (məs. 1A ➔ 2A, 5B ➔ 6B)\\n- Şagirdlər avtomatik yeni sinfə keçəcək\\n- 11-ci siniflər məzun olacaq')) return;
        try {
          const res = await fetch(`/api/admin/schools/${sId}/promote-all-classes`, { method: 'POST' });
          const d = await res.json();
          if (res.ok) {
            this.showToast(d.message);
            await this.loadAllClasses();
            await this.loadAdminOverview();
          } else {
            this.showToast(d.detail || 'Xəta baş verdi', 'error');
          }
        } catch(e) {
          this.showToast('Xəta baş verdi', 'error');
        }
      },

      async adminQuickAddIndex(grade) {'''

assert old_methods_anchor in text, "old_methods_anchor not found"
text = text.replace(old_methods_anchor, new_methods, 1)

with open(path, "w", encoding="utf-8") as f:
    f.write(text)

print("SUCCESS: index.html fully upgraded!")
