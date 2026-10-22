import os

index_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "index.html")
with open(index_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Home Action Cards: 3 cards (Şagird, Müəllim, Direktor)
old_home_cards = '''      <!-- Action Cards -->
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-5 pt-2">
        
        <!-- ŞAGİRD GİRİŞİ -->
        <div class="bg-white border-2 border-slate-200 hover:border-sky-400 rounded-3xl p-6 shadow-sm hover:shadow-xl transition-all flex flex-col justify-between h-64">
          <div>
            <div class="w-12 h-12 rounded-2xl bg-sky-100 text-sky-600 flex items-center justify-center mb-3">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/></svg>
            </div>
            <h2 class="text-xl font-black text-slate-900">Şagird Portalı</h2>
            <p class="text-xs text-slate-500 mt-1 leading-relaxed">
              Məktəbinizi seçib qeydiyyatdan keçin. Müəllim sizi sinfə əlavə etdikdən sonra ev tapşırıqları və KSQ ballarınıza baxın.
            </p>
          </div>
          <div class="flex items-center gap-2 pt-4 border-t border-slate-100">
            <button @click="openAuthModal('student', 'login')" class="touch-btn flex-1 py-2.5 bg-sky-600 hover:bg-sky-700 text-white rounded-xl text-xs font-bold text-center">
              Daxil Ol
            </button>
            <button @click="openAuthModal('student', 'register')" class="touch-btn flex-1 py-2.5 bg-sky-50 hover:bg-sky-100 text-sky-700 border border-sky-200 rounded-xl text-xs font-bold text-center">
              Qeydiyyat
            </button>
          </div>
        </div>

        <!-- MÜƏLLİM GİRİŞİ -->
        <div class="bg-white border-2 border-slate-200 hover:border-violet-400 rounded-3xl p-6 shadow-sm hover:shadow-xl transition-all flex flex-col justify-between h-64">
          <div>
            <div class="w-12 h-12 rounded-2xl bg-violet-100 text-violet-600 flex items-center justify-center mb-3">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z"/></svg>
            </div>
            <h2 class="text-xl font-black text-slate-900">Müəllim Kabineti</h2>
            <p class="text-xs text-slate-500 mt-1 leading-relaxed">
              Müəllimlər üçün: Məktəbinizi seçin, sinif rəhbəri və fənn jurnallarınızı idarə edin, uşaqları sinfə əlavə edin.
            </p>
          </div>
          <div class="flex items-center gap-2 pt-4 border-t border-slate-100">
            <button @click="openAuthModal('teacher', 'login')" class="touch-btn flex-1 py-2.5 bg-violet-600 hover:bg-violet-700 text-white rounded-xl text-xs font-bold text-center">
              Daxil Ol
            </button>
            <button @click="openAuthModal('teacher', 'register')" class="touch-btn flex-1 py-2.5 bg-violet-50 hover:bg-violet-100 text-violet-700 border border-violet-200 rounded-xl text-xs font-bold text-center">
              Müəllim Qeydiyyatı
            </button>
          </div>
        </div>

      </div>

      <!-- Admin Entry Button -->
      <div class="pt-4 text-center">
        <button @click="openAdminLogin" 
                class="touch-btn inline-flex items-center gap-2 px-5 py-2.5 rounded-2xl bg-purple-50 text-purple-800 border border-purple-200 hover:bg-purple-100 text-xs font-bold shadow-sm transition-all">
          <span>🛡️ İnzibatçı (Super Admin) Girişi</span>
        </button>
      </div>'''

new_home_cards = '''      <!-- Action Cards (3 Pillars: Şagird, Müəllim, Məktəb Direktoru) -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-5 pt-2">
        
        <!-- 1. ŞAGİRD GİRİŞİ -->
        <div class="bg-white border-2 border-slate-200 hover:border-sky-400 rounded-3xl p-6 shadow-sm hover:shadow-xl transition-all flex flex-col justify-between h-72">
          <div>
            <div class="w-12 h-12 rounded-2xl bg-sky-100 text-sky-600 flex items-center justify-center mb-3">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/></svg>
            </div>
            <h2 class="text-xl font-black text-slate-900">Şagird Portalı</h2>
            <p class="text-xs text-slate-500 mt-1 leading-relaxed">
              Şəhər/rayon və məktəbinizi seçib qeydiyyatdan keçin. Ev tapşırıqları, davamiyyət və KSQ qiymətlərinizi izləyin.
            </p>
          </div>
          <div class="flex items-center gap-2 pt-4 border-t border-slate-100">
            <button @click="openAuthModal('student', 'login')" class="touch-btn flex-1 py-2.5 bg-sky-600 hover:bg-sky-700 text-white rounded-xl text-xs font-bold text-center">
              Daxil Ol
            </button>
            <button @click="openAuthModal('student', 'register')" class="touch-btn flex-1 py-2.5 bg-sky-50 hover:bg-sky-100 text-sky-700 border border-sky-200 rounded-xl text-xs font-bold text-center">
              Qeydiyyat
            </button>
          </div>
        </div>

        <!-- 2. MÜƏLLİM GİRİŞİ -->
        <div class="bg-white border-2 border-slate-200 hover:border-violet-400 rounded-3xl p-6 shadow-sm hover:shadow-xl transition-all flex flex-col justify-between h-72">
          <div>
            <div class="w-12 h-12 rounded-2xl bg-violet-100 text-violet-600 flex items-center justify-center mb-3">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z"/></svg>
            </div>
            <h2 class="text-xl font-black text-slate-900">Müəllim Kabineti</h2>
            <p class="text-xs text-slate-500 mt-1 leading-relaxed">
              Məktəbinizi seçin, sinif rəhbəri və fənn jurnallarınızı aparın, şagirdlərinizi sinfə əlavə edin, qiymətləndirmə aparın.
            </p>
          </div>
          <div class="flex items-center gap-2 pt-4 border-t border-slate-100">
            <button @click="openAuthModal('teacher', 'login')" class="touch-btn flex-1 py-2.5 bg-violet-600 hover:bg-violet-700 text-white rounded-xl text-xs font-bold text-center">
              Daxil Ol
            </button>
            <button @click="openAuthModal('teacher', 'register')" class="touch-btn flex-1 py-2.5 bg-violet-50 hover:bg-violet-100 text-violet-700 border border-violet-200 rounded-xl text-xs font-bold text-center">
              Qeydiyyat
            </button>
          </div>
        </div>

        <!-- 3. MƏKTƏB DİREKTORU GİRİŞİ -->
        <div class="bg-white border-2 border-emerald-200 hover:border-emerald-500 rounded-3xl p-6 shadow-sm hover:shadow-xl transition-all flex flex-col justify-between h-72">
          <div>
            <div class="w-12 h-12 rounded-2xl bg-emerald-100 text-emerald-700 flex items-center justify-center mb-3">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg>
            </div>
            <h2 class="text-xl font-black text-slate-900">Məktəb Direktoru</h2>
            <p class="text-xs text-slate-500 mt-1 leading-relaxed">
              Məktəbin rəhbəri üçün: Rəhbəri olduğunuz məktəbi seçin, müəllim və şagird heyətinə, siniflərə və jurnallara rəhbərlik edin.
            </p>
          </div>
          <div class="flex items-center gap-2 pt-4 border-t border-slate-100">
            <button @click="openAuthModal('director', 'login')" class="touch-btn flex-1 py-2.5 bg-emerald-700 hover:bg-emerald-800 text-white rounded-xl text-xs font-bold text-center shadow-md">
              Daxil Ol
            </button>
            <button @click="openAuthModal('director', 'register')" class="touch-btn flex-1 py-2.5 bg-emerald-50 hover:bg-emerald-100 text-emerald-800 border border-emerald-300 rounded-xl text-xs font-bold text-center">
              Direktor Qeydiyyatı
            </button>
          </div>
        </div>

      </div>

      <!-- Super Admin Entry Button (Distinct from Director) -->
      <div class="pt-6 text-center">
        <div class="inline-block bg-purple-50 border border-purple-200 rounded-2xl p-3 shadow-sm max-w-md mx-auto">
          <p class="text-[11px] text-purple-700 font-semibold mb-2">
            * Admin məktəb direktoru deyil — Respublika üzrə bütün məktəblərin Baş İnzibatçısıdır.
          </p>
          <button @click="openAdminLogin" 
                  class="touch-btn w-full py-2 bg-purple-900 hover:bg-purple-950 text-white rounded-xl text-xs font-black shadow-md flex items-center justify-center gap-2">
            <span>🛡️ Respublika Super Admin Girişi (Mirzəliyeva Əsma)</span>
          </button>
        </div>
      </div>'''

assert old_home_cards in content, "old_home_cards not found"
content = content.replace(old_home_cards, new_home_cards, 1)

# 2. Update Header User Role text to include Director
old_header_role = '''            <p class="text-[10px] font-bold uppercase tracking-wider mt-0.5" 
               :class="currentUser.role === 'admin' ? 'text-purple-600' : (currentUser.is_moderator ? 'text-amber-600' : (currentUser.role === 'teacher' ? 'text-violet-600' : 'text-sky-600'))">
              {{ currentUser.role === 'admin' ? 'Super Admin' : (currentUser.is_moderator ? 'Məktəb Nəzarətçisi' : (currentUser.role === 'teacher' ? 'Müəllim' : 'Şagird')) }}
            </p>'''

new_header_role = '''            <p class="text-[10px] font-bold uppercase tracking-wider mt-0.5" 
               :class="currentUser.role === 'admin' ? 'text-purple-600' : (currentUser.role === 'director' ? 'text-emerald-700' : (currentUser.is_moderator ? 'text-amber-600' : (currentUser.role === 'teacher' ? 'text-violet-600' : 'text-sky-600')))">
              {{ currentUser.role === 'admin' ? 'Respublika Super Admin' : (currentUser.role === 'director' ? 'Məktəb Direktoru' : (currentUser.is_moderator ? 'Məktəb Nəzarətçisi' : (currentUser.role === 'teacher' ? 'Müəllim' : 'Şagird'))) }}
            </p>'''

assert old_header_role in content, "old_header_role not found"
content = content.replace(old_header_role, new_header_role, 1)

# Allow Director to also change password in header:
old_change_btn = '''<button v-if="currentUser.role === 'admin' || currentUser.role === 'teacher'"'''
new_change_btn = '''<button v-if="currentUser.role === 'admin' || currentUser.role === 'director' || currentUser.role === 'teacher'"'''
assert old_change_btn in content, "old_change_btn not found"
content = content.replace(old_change_btn, new_change_btn, 1)

# 3. Update Admin View condition so that Directors also have their full School Dashboard!
old_admin_view_cond = '''    <!-- ==================== VIEW 2: SUPER ADMIN & MƏKTƏB NƏZARƏTÇİSİ PANELİ ==================== -->
    <div v-if="(currentView === 'admin' || (currentUser && currentUser.is_moderator)) && currentUser" class="space-y-6">'''

new_admin_view_cond = '''    <!-- ==================== VIEW 2: SUPER ADMIN & MƏKTƏB DİREKTORU PANELİ ==================== -->
    <div v-if="(currentView === 'admin' || currentView === 'director' || (currentUser && (currentUser.role === 'director' || currentUser.is_moderator))) && currentUser" class="space-y-6">'''

assert old_admin_view_cond in content, "old_admin_view_cond not found"
content = content.replace(old_admin_view_cond, new_admin_view_cond, 1)

# 4. Update Admin Banner title & role badge
old_banner_title = '''            <span class="text-xs font-black uppercase tracking-widest text-purple-300 bg-white/10 px-3 py-1 rounded-full">
              {{ currentUser.role === 'admin' ? 'Respublika Super Admin' : 'Məktəb Nəzarətçisi (Köməkçi)' }}
            </span>
            <span v-if="currentUser.school_name" class="text-xs text-purple-200 bg-white/5 px-2.5 py-0.5 rounded-full">
              📍 {{ currentUser.school_name }}
            </span>
          </div>
          <h2 class="text-2xl sm:text-3xl font-black mt-2">Məktəb İdarəetmə Mərkəzi</h2>
          <p class="text-xs text-purple-200 mt-1">
            {{ currentUser.role === 'admin' ? 'Bütün məktəblər, köməkçilər, müəllimlər və şagirdlərə nəzarət' : 'Öz məktəbinizin təsdiqləri və siniflərinə nəzarət' }}
          </p>
          <div class="mt-3 flex items-center gap-2">
            <button @click="openChangePasswordModal" class="touch-btn px-3 py-1.5 bg-white/15 hover:bg-white/25 text-white rounded-xl text-xs font-bold border border-white/20 flex items-center gap-1.5 shadow-sm">
              <span>🔑</span>
              <span>Admin Şifrəmi Dəyiş</span>
            </button>
          </div>'''

new_banner_title = '''            <span class="text-xs font-black uppercase tracking-widest px-3 py-1 rounded-full"
                  :class="currentUser.role === 'admin' ? 'text-purple-300 bg-purple-500/20' : 'text-emerald-300 bg-emerald-500/20'">
              {{ currentUser.role === 'admin' ? 'Respublika Super Admini' : (currentUser.role === 'director' ? 'Məktəb Direktoru' : 'Məktəb Nəzarətçisi') }}
            </span>
            <span v-if="currentUser.school_name" class="text-xs text-purple-200 bg-white/10 px-2.5 py-0.5 rounded-full">
              📍 {{ currentUser.school_name }} ({{ currentUser.school_region }})
            </span>
          </div>
          <h2 class="text-2xl sm:text-3xl font-black mt-2">
            {{ currentUser.role === 'admin' ? 'Respublika Super Admin İdarəetmə Mərkəzi' : currentUser.school_name + ' - Direktor Kabineti' }}
          </h2>
          <p class="text-xs text-purple-200 mt-1">
            {{ currentUser.role === 'admin' ? 'Bütün 76 şəhər/rayon, bütün məktəblər, direktorlar və istifadəçilərə mərkəzi nəzarət' : 'Rəhbərlik etdiyiniz məktəbin müəllim və şagird heyəti, təsdiqlər və sinif jurnalları' }}
          </p>
          <div class="mt-3 flex items-center gap-2">
            <button @click="openChangePasswordModal" class="touch-btn px-3 py-1.5 bg-white/15 hover:bg-white/25 text-white rounded-xl text-xs font-bold border border-white/20 flex items-center gap-1.5 shadow-sm">
              <span>🔑</span>
              <span>{{ currentUser.role === 'admin' ? 'Admin Şifrəmi Dəyiş' : 'Direktor Şifrəmi Dəyiş' }}</span>
            </button>
          </div>'''

assert old_banner_title in content, "old_banner_title not found"
content = content.replace(old_banner_title, new_banner_title, 1)

# 5. Auth Modal Title & Forms: Add Director and Cascading Region/School Selectors
old_auth_modal_title = '''        <h3 class="text-xl font-black text-slate-900">
          {{ authRole === 'admin' ? '🛡️ İnzibatçı (Super Admin)' : (authRole === 'student' ? 'Şagird' : 'Müəllim') }} Girişi
        </h3>'''

new_auth_modal_title = '''        <h3 class="text-xl font-black text-slate-900">
          {{ authRole === 'admin' ? '🛡️ Super Admin Girişi' : (authRole === 'director' ? '🏛️ Məktəb Direktoru' : (authRole === 'student' ? '👦 Şagird' : '👩‍🏫 Müəllim')) }} {{ authAction === 'login' ? 'Girişi' : 'Qeydiyyatı' }}
        </h3>'''

assert old_auth_modal_title in content, "old_auth_modal_title not found"
content = content.replace(old_auth_modal_title, new_auth_modal_title, 1)

# Replace Student and Teacher registration forms with CASCADING Rayon -> Schools dropdowns and add Director Registration
old_reg_forms = '''      <!-- Student Register Form with School Directory -->
      <form v-else-if="authRole === 'student'" @submit.prevent="handleStudentRegister" class="space-y-3">
        <!-- School Select -->
        <div>
          <label class="block text-xs font-bold text-slate-700 mb-1">🏫 Məktəbiniz (Respublika üzrə)</label>
          <select v-model="studentRegForm.school_id" required class="w-full bg-brand-50/50 border border-brand-300 rounded-xl px-3 py-2 text-xs font-medium">
            <option v-for="s in allSchoolsList" :key="s.id" :value="s.id">{{ s.name }} ({{ s.region }})</option>
          </select>
        </div>

        <div>
          <label class="block text-xs font-semibold text-slate-600 mb-1">Ad və Soyadınız</label>
          <input type="text" v-model="studentRegForm.full_name" required placeholder="Məs. Əliyev Murad" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-xs">
        </div>
        <div>
          <label class="block text-xs font-semibold text-slate-600 mb-1">İstifadəçi Adı</label>
          <input type="text" v-model="studentRegForm.username" required placeholder="Məs. murad31" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-xs">
        </div>
        <div>
          <label class="block text-xs font-semibold text-slate-600 mb-1">Şifrə</label>
          <input type="password" v-model="studentRegForm.password" required placeholder="Şifrənizi təyin edin" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-xs">
        </div>
        <button type="submit" :disabled="isSubmitting" class="touch-btn w-full py-2.5 bg-sky-600 hover:bg-sky-700 text-white font-bold rounded-xl text-xs shadow-md">
          {{ isSubmitting ? 'Yaradılır...' : 'Şagird Hesabı Yarat' }}
        </button>
      </form>

      <!-- Teacher Register Form with School Directory -->
      <form v-else @submit.prevent="handleTeacherRegister" class="space-y-3">
        <!-- School Select -->
        <div>
          <label class="block text-xs font-bold text-slate-700 mb-1">🏫 Tədris Etdiyiniz Məktəb</label>
          <select v-model="teacherRegForm.school_id" required class="w-full bg-brand-50/50 border border-brand-300 rounded-xl px-3 py-2 text-xs font-medium">
            <option v-for="s in allSchoolsList" :key="s.id" :value="s.id">{{ s.name }} ({{ s.region }})</option>
          </select>
        </div>

        <div>
          <label class="block text-xs font-semibold text-slate-600 mb-1">Ad və Soyadınız</label>
          <input type="text" v-model="teacherRegForm.full_name" required placeholder="Məs. Məmmədova Leyla" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-xs">
        </div>
        <div>
          <label class="block text-xs font-semibold text-slate-600 mb-1">Fənniniz</label>
          <input type="text" v-model="teacherRegForm.subject" required placeholder="Məs. Riyaziyyat" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-xs">
        </div>
        <div>
          <label class="block text-xs font-semibold text-slate-600 mb-1">İstifadəçi Adı</label>
          <input type="text" v-model="teacherRegForm.username" required placeholder="Məs. leyla31" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-xs">
        </div>
        <div>
          <label class="block text-xs font-semibold text-slate-600 mb-1">Şifrə</label>
          <input type="password" v-model="teacherRegForm.password" required placeholder="Şifrəniz" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-xs">
        </div>
        <button type="submit" :disabled="isSubmitting" class="touch-btn w-full py-2.5 bg-violet-600 hover:bg-violet-700 text-white font-bold rounded-xl text-xs shadow-md">
          {{ isSubmitting ? 'Yaradılır...' : 'Müəllim Hesabı Yarat' }}
        </button>
      </form>'''

new_reg_forms = '''      <!-- 1. Student Register Form with Cascading Region & Schools Directory -->
      <form v-else-if="authRole === 'student'" @submit.prevent="handleStudentRegister" class="space-y-3">
        <!-- 1. Step: Rayon / Şəhər Select -->
        <div>
          <label class="block text-xs font-bold text-slate-700 mb-1">📍 1. Şəhər və ya Rayon Seçin</label>
          <select v-model="registrationSelectedRegion" @change="onRegistrationRegionChange" required 
                  class="w-full bg-sky-50/50 border border-sky-300 rounded-xl px-3 py-2 text-xs font-bold text-sky-900 focus:ring-2 focus:ring-sky-500">
            <option value="">Şəhər və ya Rayon seçin (Respublika üzrə {{ allRegions.length }} rayon)...</option>
            <option v-for="r in allRegions" :key="r" :value="r">{{ r }}</option>
          </select>
        </div>

        <!-- 2. Step: Selected Region's Schools -->
        <div v-if="registrationSelectedRegion">
          <label class="block text-xs font-bold text-slate-700 mb-1">
            🏫 2. Məktəbinizi Seçin ({{ registrationSelectedRegion }} üzrə {{ regionSchoolsList.length }} məktəb)
          </label>
          <input type="text" v-model="schoolSearchQuery" placeholder="Məktəb axtar (məs. 31)..." 
                 class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-1.5 text-xs mb-1.5">
          <select v-model="studentRegForm.school_id" required 
                  class="w-full bg-white border border-slate-300 rounded-xl px-3 py-2 text-xs font-medium focus:ring-2 focus:ring-sky-500">
            <option value="">Məktəb seçin...</option>
            <option v-for="s in filteredRegionSchools" :key="s.id" :value="s.id">{{ s.name }}</option>
          </select>
        </div>
        <div v-else class="p-2.5 bg-slate-50 border border-dashed border-slate-300 rounded-xl text-[11px] text-slate-500 text-center">
          * Məktəblərin tam siyahısını görmək üçün əvvəlcə Şəhər/Rayon seçin
        </div>

        <div>
          <label class="block text-xs font-semibold text-slate-600 mb-1">Ad və Soyadınız</label>
          <input type="text" v-model="studentRegForm.full_name" required placeholder="Məs. Əliyev Murad" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-xs">
        </div>
        <div>
          <label class="block text-xs font-semibold text-slate-600 mb-1">İstifadəçi Adı</label>
          <input type="text" v-model="studentRegForm.username" required placeholder="Məs. murad31" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-xs">
        </div>
        <div>
          <label class="block text-xs font-semibold text-slate-600 mb-1">Şifrə</label>
          <input type="password" v-model="studentRegForm.password" required placeholder="Şifrənizi təyin edin" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-xs">
        </div>
        <button type="submit" :disabled="isSubmitting" class="touch-btn w-full py-2.5 bg-sky-600 hover:bg-sky-700 text-white font-bold rounded-xl text-xs shadow-md">
          {{ isSubmitting ? 'Yaradılır...' : 'Şagird Hesabı Yarat' }}
        </button>
      </form>

      <!-- 2. Director Register Form with Cascading Region & Schools Directory -->
      <form v-else-if="authRole === 'director'" @submit.prevent="handleDirectorRegister" class="space-y-3">
        <!-- 1. Step: Rayon / Şəhər Select -->
        <div>
          <label class="block text-xs font-bold text-emerald-900 mb-1">📍 1. Şəhər və ya Rayon Seçin</label>
          <select v-model="registrationSelectedRegion" @change="onRegistrationRegionChange" required 
                  class="w-full bg-emerald-50/50 border border-emerald-300 rounded-xl px-3 py-2 text-xs font-bold text-emerald-900 focus:ring-2 focus:ring-emerald-500">
            <option value="">Şəhər və ya Rayon seçin ({{ allRegions.length }} rayon)...</option>
            <option v-for="r in allRegions" :key="r" :value="r">{{ r }}</option>
          </select>
        </div>

        <!-- 2. Step: Selected Region's Schools -->
        <div v-if="registrationSelectedRegion">
          <label class="block text-xs font-bold text-emerald-900 mb-1">
            🏛️ 2. Rəhbəri Olduğunuz Məktəbi Seçin ({{ regionSchoolsList.length }} məktəb)
          </label>
          <input type="text" v-model="schoolSearchQuery" placeholder="Məktəb adı və ya nömrəsi ilə axtar..." 
                 class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-1.5 text-xs mb-1.5">
          <select v-model="directorRegForm.school_id" required 
                  class="w-full bg-white border border-slate-300 rounded-xl px-3 py-2 text-xs font-medium focus:ring-2 focus:ring-emerald-500">
            <option value="">Direktor olduğunuz məktəbi seçin...</option>
            <option v-for="s in filteredRegionSchools" :key="s.id" :value="s.id">{{ s.name }}</option>
          </select>
        </div>
        <div v-else class="p-2.5 bg-slate-50 border border-dashed border-slate-300 rounded-xl text-[11px] text-slate-500 text-center">
          * Məktəbləri görmək üçün əvvəlcə yuxarıdan Şəhər/Rayon seçin
        </div>

        <div>
          <label class="block text-xs font-semibold text-slate-600 mb-1">Direktorun Adı və Soyadı</label>
          <input type="text" v-model="directorRegForm.full_name" required placeholder="Məs. Əhmədov Rasim" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-xs">
        </div>
        <div>
          <label class="block text-xs font-semibold text-slate-600 mb-1">Əlaqə Telefonu</label>
          <input type="text" v-model="directorRegForm.phone" placeholder="Məs. 050-123-45-67" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-xs">
        </div>
        <div>
          <label class="block text-xs font-semibold text-slate-600 mb-1">İstifadəçi Adı</label>
          <input type="text" v-model="directorRegForm.username" required placeholder="Məs. rasim_direktor" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-xs">
        </div>
        <div>
          <label class="block text-xs font-semibold text-slate-600 mb-1">Şifrə</label>
          <input type="password" v-model="directorRegForm.password" required placeholder="Şifrənizi təyin edin" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-xs">
        </div>
        <button type="submit" :disabled="isSubmitting" class="touch-btn w-full py-2.5 bg-emerald-700 hover:bg-emerald-800 text-white font-bold rounded-xl text-xs shadow-md">
          {{ isSubmitting ? 'Qeydiyyat aparılır...' : 'Məktəb Direktoru Hesabı Yarat 🏛️' }}
        </button>
      </form>

      <!-- 3. Teacher Register Form with Cascading Region & Schools Directory -->
      <form v-else @submit.prevent="handleTeacherRegister" class="space-y-3">
        <!-- 1. Step: Rayon / Şəhər Select -->
        <div>
          <label class="block text-xs font-bold text-violet-900 mb-1">📍 1. Şəhər və ya Rayon Seçin</label>
          <select v-model="registrationSelectedRegion" @change="onRegistrationRegionChange" required 
                  class="w-full bg-violet-50/50 border border-violet-300 rounded-xl px-3 py-2 text-xs font-bold text-violet-900 focus:ring-2 focus:ring-violet-500">
            <option value="">Şəhər və ya Rayon seçin ({{ allRegions.length }} rayon)...</option>
            <option v-for="r in allRegions" :key="r" :value="r">{{ r }}</option>
          </select>
        </div>

        <!-- 2. Step: Selected Region's Schools -->
        <div v-if="registrationSelectedRegion">
          <label class="block text-xs font-bold text-violet-900 mb-1">
            🏫 2. Tədris Etdiyiniz Məktəbi Seçin ({{ regionSchoolsList.length }} məktəb)
          </label>
          <input type="text" v-model="schoolSearchQuery" placeholder="Məktəb axtar (məs. 31)..." 
                 class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-1.5 text-xs mb-1.5">
          <select v-model="teacherRegForm.school_id" required 
                  class="w-full bg-white border border-slate-300 rounded-xl px-3 py-2 text-xs font-medium focus:ring-2 focus:ring-violet-500">
            <option value="">Məktəb seçin...</option>
            <option v-for="s in filteredRegionSchools" :key="s.id" :value="s.id">{{ s.name }}</option>
          </select>
        </div>
        <div v-else class="p-2.5 bg-slate-50 border border-dashed border-slate-300 rounded-xl text-[11px] text-slate-500 text-center">
          * Məktəbləri görmək üçün əvvəlcə yuxarıdan Şəhər/Rayon seçin
        </div>

        <div>
          <label class="block text-xs font-semibold text-slate-600 mb-1">Ad və Soyadınız</label>
          <input type="text" v-model="teacherRegForm.full_name" required placeholder="Məs. Məmmədova Leyla" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-xs">
        </div>
        <div>
          <label class="block text-xs font-semibold text-slate-600 mb-1">Fənniniz</label>
          <input type="text" v-model="teacherRegForm.subject" required placeholder="Məs. Riyaziyyat" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-xs">
        </div>
        <div>
          <label class="block text-xs font-semibold text-slate-600 mb-1">İstifadəçi Adı</label>
          <input type="text" v-model="teacherRegForm.username" required placeholder="Məs. leyla31" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-xs">
        </div>
        <div>
          <label class="block text-xs font-semibold text-slate-600 mb-1">Şifrə</label>
          <input type="password" v-model="teacherRegForm.password" required placeholder="Şifrəniz" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-xs">
        </div>
        <button type="submit" :disabled="isSubmitting" class="touch-btn w-full py-2.5 bg-violet-600 hover:bg-violet-700 text-white font-bold rounded-xl text-xs shadow-md">
          {{ isSubmitting ? 'Yaradılır...' : 'Müəllim Hesabı Yarat' }}
        </button>
      </form>'''

assert old_reg_forms in content, "old_reg_forms not found"
content = content.replace(old_reg_forms, new_reg_forms, 1)

# 6. Add Vue Data properties for Director & Cascading Region Schools
old_vue_data = '''        studentRegForm: { full_name: '', username: '', password: '', school_id: 1 },
        teacherRegForm: { full_name: '', subject: '', username: '', password: '', school_id: 1, class_head_id: null },'''

new_vue_data = '''        studentRegForm: { full_name: '', username: '', password: '', school_id: '' },
        teacherRegForm: { full_name: '', subject: '', username: '', password: '', school_id: '', class_head_id: null },
        directorRegForm: { full_name: '', username: '', password: '', phone: '', school_id: '' },
        registrationSelectedRegion: '',
        regionSchoolsList: [],
        schoolSearchQuery: '','''

assert old_vue_data in content, "old_vue_data not found"
content = content.replace(old_vue_data, new_vue_data, 1)

# 7. Add computed property `filteredRegionSchools`
old_computed_anchor = '''    data() {'''

new_computed = '''    computed: {
      filteredRegionSchools() {
        if (!this.schoolSearchQuery.trim()) return this.regionSchoolsList;
        const q = this.schoolSearchQuery.toLowerCase().trim();
        return this.regionSchoolsList.filter(s => s.name.toLowerCase().includes(q));
      }
    },
    data() {'''

assert old_computed_anchor in content, "old_computed_anchor not found"
content = content.replace(old_computed_anchor, new_computed, 1)

# 8. Add methods for Region change & Director registration
old_methods_anchor = '''      async loadSchoolsDirectory() {'''

new_methods_anchor = '''      async onRegistrationRegionChange() {
        this.schoolSearchQuery = '';
        if (!this.registrationSelectedRegion) {
          this.regionSchoolsList = [];
          return;
        }
        try {
          const res = await fetch('/api/schools?region=' + encodeURIComponent(this.registrationSelectedRegion));
          this.regionSchoolsList = await res.json();
          this.studentRegForm.school_id = '';
          this.teacherRegForm.school_id = '';
          this.directorRegForm.school_id = '';
        } catch(e) {
          console.error(e);
        }
      },

      async handleDirectorRegister() {
        if (!this.directorRegForm.school_id) {
          this.showToast('Zəhmət olmasa rəhbəri olduğunuz məktəbi seçin!', 'error');
          return;
        }
        this.isSubmitting = true;
        try {
          const res = await fetch('/api/auth/register-director', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(this.directorRegForm)
          });
          const d = await res.json();
          if (!res.ok) throw new Error(d.detail || 'Qeydiyyat xətası');
          this.showToast(d.message);
          this.showAuthModal = false;
        } catch(e) {
          this.showToast(e.message, 'error');
        } finally {
          this.isSubmitting = false;
        }
      },

      async loadSchoolsDirectory() {'''

assert old_methods_anchor in content, "old_methods_anchor not found"
content = content.replace(old_methods_anchor, new_methods_anchor, 1)

# 9. Update openAuthModal to reset region selection & handle director
old_open_auth = '''      openAuthModal(role, action) {
        this.authRole = role;
        this.authAction = action;
        this.loginForm = { username: '', password: '' };
        this.showAuthModal = true;
      },'''

new_open_auth = '''      openAuthModal(role, action) {
        this.authRole = role;
        this.authAction = action;
        this.loginForm = { username: '', password: '' };
        this.registrationSelectedRegion = '';
        this.regionSchoolsList = [];
        this.schoolSearchQuery = '';
        this.showAuthModal = true;
      },'''

assert old_open_auth in content, "old_open_auth not found"
content = content.replace(old_open_auth, new_open_auth, 1)

# 10. Update mounted session restore for Director
old_mount_session = '''          if (this.currentUser.role === 'admin' || this.currentUser.is_moderator) {
            this.currentView = 'admin';
            await this.loadAdminData();
          } else if (this.currentUser.role === 'teacher') {'''

new_mount_session = '''          if (this.currentUser.role === 'admin') {
            this.currentView = 'admin';
            await this.loadAdminData();
          } else if (this.currentUser.role === 'director' || this.currentUser.is_moderator) {
            this.currentView = 'director';
            this.selectedAdminSchoolId = this.currentUser.school_id;
            await this.loadAdminData();
          } else if (this.currentUser.role === 'teacher') {'''

assert old_mount_session in content, "old_mount_session not found"
content = content.replace(old_mount_session, new_mount_session, 1)

# 11. Update handleLogin session setup for Director
old_login_handler = '''          if (this.currentUser.role === 'admin' || this.currentUser.is_moderator) {
            this.currentView = 'admin';
            await this.loadAdminData();
          } else if (this.currentUser.role === 'teacher') {'''

new_login_handler = '''          if (this.currentUser.role === 'admin') {
            this.currentView = 'admin';
            await this.loadAdminData();
          } else if (this.currentUser.role === 'director' || this.currentUser.is_moderator) {
            this.currentView = 'director';
            this.selectedAdminSchoolId = this.currentUser.school_id;
            await this.loadAdminData();
          } else if (this.currentUser.role === 'teacher') {'''

assert old_login_handler in content, "old_login_handler not found"
content = content.replace(old_login_handler, new_login_handler, 1)

# 12. Update goHome for Director
old_go_home = '''          if (this.currentUser.role === 'admin' || this.currentUser.is_moderator) this.currentView = 'admin';
          else if (this.currentUser.role === 'teacher') this.currentView = 'teacher';'''

new_go_home = '''          if (this.currentUser.role === 'admin') this.currentView = 'admin';
          else if (this.currentUser.role === 'director' || this.currentUser.is_moderator) this.currentView = 'director';
          else if (this.currentUser.role === 'teacher') this.currentView = 'teacher';'''

assert old_go_home in content, "old_go_home not found"
content = content.replace(old_go_home, new_go_home, 1)

with open(index_path, "w", encoding="utf-8") as f:
    f.write(content)

print("SUCCESS: Director portal and cascading 76-region school directory successfully integrated!")
