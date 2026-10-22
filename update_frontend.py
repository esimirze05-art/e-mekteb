import os

index_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "index.html")
with open(index_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Brand Logo
old_logo = '''      <!-- Brand Logo -->
      <a href="#" @click.prevent="goHome" class="flex items-center gap-3 group">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-700 to-brand-500 flex items-center justify-center text-white shadow-md shadow-brand-500/20 group-hover:scale-105 transition-transform">
          <svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M22 10v6M2 10l10-5 10 5-10 5z"/>
            <path d="M6 12v5c3 3 9 3 12 0v-5"/>
          </svg>
        </div>'''

new_logo = '''      <!-- Brand Logo -->
      <a href="#" @click.prevent="goHome" class="flex items-center gap-3 group">
        <img src="/static/logo.png" onerror="this.src='/static/icon.svg'" alt="E.məktəb Logo" class="w-10 h-10 rounded-xl object-cover shadow-md shadow-brand-500/20 group-hover:scale-105 transition-transform border border-amber-300/40">'''

assert old_logo in content, "old_logo not found"
content = content.replace(old_logo, new_logo, 1)

# 2. Header user actions (add Change Password button)
old_user_hdr = '''          <div class="text-right hidden sm:block">
            <p class="text-xs font-bold text-slate-800 leading-none">{{ currentUser.full_name }}</p>
            <p class="text-[10px] font-bold uppercase tracking-wider mt-0.5" 
               :class="currentUser.role === 'admin' ? 'text-purple-600' : (currentUser.is_moderator ? 'text-amber-600' : (currentUser.role === 'teacher' ? 'text-violet-600' : 'text-sky-600'))">
              {{ currentUser.role === 'admin' ? 'Super Admin' : (currentUser.is_moderator ? 'Məktəb Nəzarətçisi' : (currentUser.role === 'teacher' ? 'Müəllim' : 'Şagird')) }}
            </p>
          </div>
          <button @click="logout" title="Çıxış"'''

new_user_hdr = '''          <div class="text-right hidden sm:block">
            <p class="text-xs font-bold text-slate-800 leading-none">{{ currentUser.full_name }}</p>
            <p class="text-[10px] font-bold uppercase tracking-wider mt-0.5" 
               :class="currentUser.role === 'admin' ? 'text-purple-600' : (currentUser.is_moderator ? 'text-amber-600' : (currentUser.role === 'teacher' ? 'text-violet-600' : 'text-sky-600'))">
              {{ currentUser.role === 'admin' ? 'Super Admin' : (currentUser.is_moderator ? 'Məktəb Nəzarətçisi' : (currentUser.role === 'teacher' ? 'Müəllim' : 'Şagird')) }}
            </p>
          </div>
          <button v-if="currentUser.role === 'admin' || currentUser.role === 'teacher'" 
                  @click="openChangePasswordModal" 
                  title="Şifrəmi Dəyiş" 
                  class="touch-btn px-2.5 py-1.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold border border-slate-300 transition-colors flex items-center gap-1 shadow-sm">
            <span>🔑</span>
            <span class="hidden md:inline">Şifrəni Dəyiş</span>
          </button>
          <button @click="logout" title="Çıxış"'''

assert old_user_hdr in content, "old_user_hdr not found"
content = content.replace(old_user_hdr, new_user_hdr, 1)

# 3. Home welcome hero
old_hero = '''      <div class="text-center space-y-3">
        <div class="w-16 h-16 rounded-2xl bg-brand-50 text-brand-600 flex items-center justify-center mx-auto shadow-sm border border-brand-100">
          <svg class="w-8 h-8" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M22 10v6M2 10l10-5 10 5-10 5z"/>
            <path d="M6 12v5c3 3 9 3 12 0v-5"/>
          </svg>
        </div>
        <h1 class="text-3xl font-black text-slate-900 tracking-tight">E.məktəb Portalı</h1>'''

new_hero = '''      <div class="text-center space-y-3">
        <img src="/static/logo.png" onerror="this.src='/static/icon.svg'" alt="E.məktəb Logo" class="w-20 h-20 rounded-3xl mx-auto shadow-lg shadow-brand-500/20 border border-amber-300/40 object-cover">
        <h1 class="text-3xl font-black text-slate-900 tracking-tight">E.məktəb Portalı</h1>'''

assert old_hero in content, "old_hero not found"
content = content.replace(old_hero, new_hero, 1)

# 4. Admin Header Banner: Add Admin Şifrəmi Dəyiş button
old_admin_hdr = '''          <h2 class="text-2xl sm:text-3xl font-black mt-2">Məktəb İdarəetmə Mərkəzi</h2>
          <p class="text-xs text-purple-200 mt-1">
            {{ currentUser.role === 'admin' ? 'Bütün məktəblər, köməkçilər, müəllimlər və şagirdlərə nəzarət' : 'Öz məktəbinizin təsdiqləri və siniflərinə nəzarət' }}
          </p>'''

new_admin_hdr = '''          <h2 class="text-2xl sm:text-3xl font-black mt-2">Məktəb İdarəetmə Mərkəzi</h2>
          <p class="text-xs text-purple-200 mt-1">
            {{ currentUser.role === 'admin' ? 'Bütün məktəblər, köməkçilər, müəllimlər və şagirdlərə nəzarət' : 'Öz məktəbinizin təsdiqləri və siniflərinə nəzarət' }}
          </p>
          <div class="mt-3 flex items-center gap-2">
            <button @click="openChangePasswordModal" class="touch-btn px-3 py-1.5 bg-white/15 hover:bg-white/25 text-white rounded-xl text-xs font-bold border border-white/20 flex items-center gap-1.5 shadow-sm">
              <span>🔑</span>
              <span>Admin Şifrəmi Dəyiş</span>
            </button>
          </div>'''

assert old_admin_hdr in content, "old_admin_hdr not found"
content = content.replace(old_admin_hdr, new_admin_hdr, 1)

# 5. Admin Overview Cards: Add Şifrə Sorğuları card
old_overview_cards = '''      <!-- Overview Stats -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div class="bg-white p-5 rounded-3xl border border-slate-200 shadow-sm">
          <p class="text-xs font-medium text-slate-500">Müəllimlər</p>
          <p class="text-3xl font-black text-violet-600 mt-1">{{ adminOverview.teachers_count }}</p>
        </div>
        <div class="bg-white p-5 rounded-3xl border border-slate-200 shadow-sm">
          <p class="text-xs font-medium text-slate-500">Şagirdlər</p>
          <p class="text-3xl font-black text-sky-600 mt-1">{{ adminOverview.students_count }}</p>
        </div>
        <div class="bg-white p-5 rounded-3xl border border-slate-200 shadow-sm">
          <p class="text-xs font-medium text-slate-500">Siniflər</p>
          <p class="text-3xl font-black text-brand-600 mt-1">{{ adminOverview.classes_count }}</p>
        </div>
        <div class="bg-white p-5 rounded-3xl border border-slate-200 shadow-sm">
          <p class="text-xs font-medium text-slate-500">Təsdiq Gözləyən</p>
          <p class="text-3xl font-black text-amber-600 mt-1">{{ adminOverview.pending_count }}</p>
        </div>
      </div>'''

new_overview_cards = '''      <!-- Overview Stats -->
      <div class="grid grid-cols-2 sm:grid-cols-5 gap-4">
        <div class="bg-white p-5 rounded-3xl border border-slate-200 shadow-sm">
          <p class="text-xs font-medium text-slate-500">Müəllimlər</p>
          <p class="text-3xl font-black text-violet-600 mt-1">{{ adminOverview.teachers_count }}</p>
        </div>
        <div class="bg-white p-5 rounded-3xl border border-slate-200 shadow-sm">
          <p class="text-xs font-medium text-slate-500">Şagirdlər</p>
          <p class="text-3xl font-black text-sky-600 mt-1">{{ adminOverview.students_count }}</p>
        </div>
        <div class="bg-white p-5 rounded-3xl border border-slate-200 shadow-sm">
          <p class="text-xs font-medium text-slate-500">Siniflər</p>
          <p class="text-3xl font-black text-brand-600 mt-1">{{ adminOverview.classes_count }}</p>
        </div>
        <div class="bg-white p-5 rounded-3xl border border-slate-200 shadow-sm">
          <p class="text-xs font-medium text-slate-500">Təsdiq Gözləyən</p>
          <p class="text-3xl font-black text-amber-600 mt-1">{{ adminOverview.pending_count }}</p>
        </div>
        <div class="bg-white p-5 rounded-3xl border border-slate-200 shadow-sm cursor-pointer hover:border-amber-400 transition-colors" @click="adminTab = 'password_resets'">
          <p class="text-xs font-medium text-slate-500">Şifrə Sorğuları</p>
          <p class="text-3xl font-black text-amber-600 mt-1">{{ adminOverview.reset_requests_count || 0 }}</p>
        </div>
      </div>'''

assert old_overview_cards in content, "old_overview_cards not found"
content = content.replace(old_overview_cards, new_overview_cards, 1)

# 6. Admin Tabs: Add Şifrə Sorğuları tab button
old_tabs_btn = '''        <button @click="adminTab = 'pending'" 
                :class="adminTab === 'pending' ? 'border-amber-500 text-amber-700 font-black bg-amber-50/50' : 'border-transparent text-slate-500'" 
                class="px-4 py-2.5 border-b-2 text-xs sm:text-sm rounded-t-xl transition-colors whitespace-nowrap flex items-center gap-2">
          <span>🔔 Təsdiq Gözləyənlər</span>
          <span v-if="adminPendingRequests.length > 0" class="px-2 py-0.5 rounded-full bg-rose-600 text-white text-[10px] font-black animate-pulse">
            {{ adminPendingRequests.length }}
          </span>
        </button>'''

new_tabs_btn = '''        <button @click="adminTab = 'pending'" 
                :class="adminTab === 'pending' ? 'border-amber-500 text-amber-700 font-black bg-amber-50/50' : 'border-transparent text-slate-500'" 
                class="px-4 py-2.5 border-b-2 text-xs sm:text-sm rounded-t-xl transition-colors whitespace-nowrap flex items-center gap-2">
          <span>🔔 Təsdiq Gözləyənlər</span>
          <span v-if="adminPendingRequests.length > 0" class="px-2 py-0.5 rounded-full bg-rose-600 text-white text-[10px] font-black animate-pulse">
            {{ adminPendingRequests.length }}
          </span>
        </button>
        <button @click="adminTab = 'password_resets'" 
                :class="adminTab === 'password_resets' ? 'border-amber-600 text-amber-800 font-black bg-amber-50/50' : 'border-transparent text-slate-500'" 
                class="px-4 py-2.5 border-b-2 text-xs sm:text-sm rounded-t-xl transition-colors whitespace-nowrap flex items-center gap-2">
          <span>🔑 Şifrə Sorğuları</span>
          <span v-if="adminPasswordResets.length > 0" class="px-2 py-0.5 rounded-full bg-amber-600 text-white text-[10px] font-black animate-pulse">
            {{ adminPasswordResets.length }}
          </span>
        </button>'''

assert old_tabs_btn in content, "old_tabs_btn not found"
content = content.replace(old_tabs_btn, new_tabs_btn, 1)

# 7. Admin Tab Content: Add Şifrə Sorğuları tab panel
old_schools_tab = '''      <!-- TAB 1: MƏKTƏBLƏR VƏ KÖMƏKÇİLƏR (NƏZARƏTÇİLƏR) -->'''

new_schools_tab = '''      <!-- TAB: ŞİFRƏ BƏRPA SORĞULARI -->
      <div v-if="adminTab === 'password_resets'" class="space-y-4">
        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-base font-bold text-slate-900 flex items-center gap-2">
              <span>🔑</span> Şifrə Bərpa Sorğuları ({{ adminPasswordResets.length }})
            </h3>
            <p class="text-xs text-slate-500">Parolunu unudan müəllim və şagirdlərin göndərdiyi müraciətlər</p>
          </div>
        </div>

        <div v-if="adminPasswordResets.length === 0" class="text-center py-12 bg-white rounded-3xl border border-dashed border-slate-300">
          <div class="w-12 h-12 rounded-2xl bg-sky-50 text-sky-600 flex items-center justify-center mx-auto mb-2 text-xl">🛡️</div>
          <p class="text-slate-700 font-bold text-sm">Hazırda şifrə bərpası üçün heç bir sorğu yoxdur.</p>
        </div>

        <div v-else class="space-y-3">
          <div v-for="resetItem in adminPasswordResets" :key="resetItem.id" 
               class="bg-white rounded-3xl p-5 border-2 border-amber-300 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <div class="flex items-center gap-2 mb-1">
                <span class="px-2.5 py-0.5 rounded-full text-[10px] font-black uppercase tracking-wider" 
                      :class="resetItem.role === 'teacher' ? 'bg-violet-100 text-violet-800' : 'bg-sky-100 text-sky-800'">
                  {{ resetItem.role === 'teacher' ? 'Müəllim' : 'Şagird' }}
                </span>
                <span class="text-xs font-bold text-brand-700 bg-brand-50 px-2 py-0.5 rounded border border-brand-200">
                  📍 {{ resetItem.school_name }}
                </span>
              </div>
              <h4 class="text-lg font-black text-slate-900">{{ resetItem.full_name }}</h4>
              <p class="text-xs text-slate-500">
                İstifadəçi adı: <strong class="text-slate-800">@{{ resetItem.username }}</strong>
                <span v-if="resetItem.contact_phone" class="ml-2">• Əlaqə: <strong class="text-slate-800">{{ resetItem.contact_phone }}</strong></span>
                <span class="ml-2 text-slate-400">({{ resetItem.created_at }})</span>
              </p>
            </div>

            <div class="flex items-center gap-2">
              <button @click="resolvePasswordReset(resetItem, '123456')" class="touch-btn px-3 py-2 bg-amber-50 hover:bg-amber-100 text-amber-800 border border-amber-300 rounded-xl text-xs font-bold" title="Standart '123456' şifrəsi təyin edir">
                ⚡ 123456 Təyin Et
              </button>
              <button @click="resolvePasswordReset(resetItem)" class="touch-btn px-4 py-2 bg-brand-600 hover:bg-brand-700 text-white rounded-xl text-xs font-bold shadow-md">
                🔑 Yeni Şifrə Təyin Et
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- TAB 1: MƏKTƏBLƏR VƏ KÖMƏKÇİLƏR (NƏZARƏTÇİLƏR) -->'''

assert old_schools_tab in content, "old_schools_tab not found"
content = content.replace(old_schools_tab, new_schools_tab, 1)

# 8. Teacher Dashboard: Add Şifrəmi Dəyiş button
old_teacher_btn = '''        <div class="flex items-center gap-2">
          <button v-if="activeTeacherClass" @click="activeTeacherClass = null" class="touch-btn px-4 py-2 rounded-xl bg-slate-100 text-slate-700 text-xs font-bold">⬅ Siniflərə Qayıt</button>
          <button @click="showAssignModal = true" class="touch-btn px-3 py-2 rounded-xl bg-brand-50 text-brand-700 text-xs font-bold border border-brand-200">⚙️ Siniflərimi Tənzimlə</button>
        </div>'''

new_teacher_btn = '''        <div class="flex items-center gap-2">
          <button @click="openChangePasswordModal" class="touch-btn px-3 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold border border-slate-300 flex items-center gap-1.5 shadow-sm">
            <span>🔑</span>
            <span>Şifrəmi Dəyiş</span>
          </button>
          <button v-if="activeTeacherClass" @click="activeTeacherClass = null" class="touch-btn px-4 py-2 rounded-xl bg-slate-100 text-slate-700 text-xs font-bold">⬅ Siniflərə Qayıt</button>
          <button @click="showAssignModal = true" class="touch-btn px-3 py-2 rounded-xl bg-brand-50 text-brand-700 text-xs font-bold border border-brand-200">⚙️ Siniflərimi Tənzimlə</button>
        </div>'''

assert old_teacher_btn in content, "old_teacher_btn not found"
content = content.replace(old_teacher_btn, new_teacher_btn, 1)

# 9. Login Form: Add Parolu unutdum? link
old_login_field = '''        <div>
          <label class="block text-xs font-semibold text-slate-600 mb-1">Şifrə</label>
          <input type="password" v-model="loginForm.password" required placeholder="Şifrəniz" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3.5 py-2.5 text-sm focus:ring-2 focus:ring-brand-500">
        </div>'''

new_login_field = '''        <div>
          <div class="flex items-center justify-between mb-1">
            <label class="block text-xs font-semibold text-slate-600">Şifrə</label>
            <button type="button" @click="openForgotPasswordModal" class="text-xs text-brand-600 hover:text-brand-800 font-bold hover:underline">
              Parolu unutdum?
            </button>
          </div>
          <input type="password" v-model="loginForm.password" required placeholder="Şifrəniz" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3.5 py-2.5 text-sm focus:ring-2 focus:ring-brand-500">
        </div>'''

assert old_login_field in content, "old_login_field not found"
content = content.replace(old_login_field, new_login_field, 1)

# 10. Modals: Add Forgot Password & Self-Change Password modals
old_modals_end = '''  <!-- Modal: Assign Classes for Teacher -->'''

new_modals = '''  <!-- Modal: Parolu Unutdum (Forgot Password) -->
  <div v-if="showForgotPasswordModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm">
    <div class="bg-white rounded-3xl p-6 sm:p-7 max-w-md w-full shadow-2xl border border-slate-100 relative">
      <button @click="showForgotPasswordModal = false" class="absolute top-5 right-5 text-slate-400 hover:text-slate-600 text-2xl font-bold">&times;</button>

      <div class="text-center mb-5">
        <div class="w-12 h-12 rounded-2xl bg-amber-50 text-amber-600 flex items-center justify-center mx-auto mb-2 text-xl font-bold border border-amber-200">
          🔑
        </div>
        <h3 class="text-lg font-black text-slate-900">Şifrəni Bərpa Et</h3>
        <p class="text-xs text-slate-500 mt-0.5">Şifrənizi unutmusunuzsa, aşağıdakı seçimlərdən istifadə edin</p>
      </div>

      <!-- Segmented Control: Müəllim/Şagird vs Admin -->
      <div class="flex bg-slate-100 p-1 rounded-2xl mb-4 text-xs font-bold">
        <button type="button" @click="forgotTab = 'user'" 
                :class="forgotTab === 'user' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500'" 
                class="flex-1 py-2 rounded-xl transition-all">
          👨‍🏫 Müəllim / Şagird
        </button>
        <button type="button" @click="forgotTab = 'admin'" 
                :class="forgotTab === 'admin' ? 'bg-purple-600 text-white shadow-sm' : 'text-slate-500'" 
                class="flex-1 py-2 rounded-xl transition-all">
          🛡️ Admin Bərpası
        </button>
      </div>

      <!-- Form: Müəllim / Şagird Sorğusu -->
      <form v-if="forgotTab === 'user'" @submit.prevent="handleForgotPasswordSubmit" class="space-y-3.5">
        <div>
          <label class="block text-xs font-semibold text-slate-700 mb-1">İstifadəçi Adınız</label>
          <input type="text" v-model="forgotUserForm.username" required placeholder="Məs. leyla31 və ya murad31" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3.5 py-2.5 text-xs font-medium focus:ring-2 focus:ring-brand-500">
        </div>
        <div>
          <label class="block text-xs font-semibold text-slate-700 mb-1">Əlaqə Telefonunuz və ya Qeydiniz</label>
          <input type="text" v-model="forgotUserForm.contact_phone" placeholder="Məs. 050-123-45-67" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3.5 py-2.5 text-xs font-medium focus:ring-2 focus:ring-brand-500">
        </div>
        <p class="text-[11px] text-slate-500 leading-relaxed bg-amber-50 p-2.5 rounded-xl border border-amber-200">
          ℹ️ Müraciətiniz sistem admininə göndəriləcək və məktəb admini sizin üçün yeni şifrə təyin edəcək.
        </p>
        <button type="submit" :disabled="isSubmitting" class="touch-btn w-full py-2.5 bg-amber-600 hover:bg-amber-700 text-white font-bold rounded-xl text-xs shadow-md shadow-amber-500/20">
          {{ isSubmitting ? 'Göndərilir...' : 'Sorğu Göndər' }}
        </button>
      </form>

      <!-- Form: Admin Bərpa Açar Sözü -->
      <form v-else @submit.prevent="handleAdminRecoverySubmit" class="space-y-3.5">
        <div>
          <label class="block text-xs font-semibold text-purple-900 mb-1">Admin Bərpa Kodu (Master Key)</label>
          <input type="password" v-model="forgotAdminForm.recovery_code" required placeholder="Bərpa açar sözünü daxil edin" class="w-full bg-purple-50/50 border border-purple-300 rounded-xl px-3.5 py-2.5 text-xs font-medium focus:ring-2 focus:ring-purple-500">
          <p class="text-[10px] text-purple-600 mt-1">İpucu: Sistem yaradıcısının təyin etdiyi xüsusi bərpa açarı</p>
        </div>
        <div>
          <label class="block text-xs font-semibold text-slate-700 mb-1">Yeni Admin Şifrəsi</label>
          <input type="password" v-model="forgotAdminForm.new_password" required placeholder="Yeni şifrəniz" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3.5 py-2.5 text-xs font-medium focus:ring-2 focus:ring-purple-500">
        </div>
        <div>
          <label class="block text-xs font-semibold text-slate-700 mb-1">Yeni Şifrənin Təkrarı</label>
          <input type="password" v-model="forgotAdminForm.confirm_password" required placeholder="Yeni şifrəni təkrar yazın" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3.5 py-2.5 text-xs font-medium focus:ring-2 focus:ring-purple-500">
        </div>
        <button type="submit" :disabled="isSubmitting" class="touch-btn w-full py-2.5 bg-purple-600 hover:bg-purple-700 text-white font-bold rounded-xl text-xs shadow-md shadow-purple-500/20">
          {{ isSubmitting ? 'Yenilənir...' : 'Admin Şifrəsini Yenilə 🛡️' }}
        </button>
      </form>
    </div>
  </div>

  <!-- Modal: Şəxsi Şifrəmi Dəyiş (Self-Change Password) -->
  <div v-if="showChangePasswordModal && currentUser" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm">
    <div class="bg-white rounded-3xl p-6 sm:p-7 max-w-md w-full shadow-2xl border border-slate-100 relative">
      <button @click="showChangePasswordModal = false" class="absolute top-5 right-5 text-slate-400 hover:text-slate-600 text-2xl font-bold">&times;</button>

      <div class="text-center mb-5">
        <div class="w-12 h-12 rounded-2xl bg-brand-50 text-brand-600 flex items-center justify-center mx-auto mb-2 text-xl font-bold border border-brand-200">
          🔒
        </div>
        <h3 class="text-lg font-black text-slate-900">Şifrəni Dəyişdir</h3>
        <p class="text-xs text-slate-500 mt-0.5">
          İstifadəçi: <strong class="text-slate-800">{{ currentUser.full_name }}</strong> (@{{ currentUser.username }})
        </p>
      </div>

      <form @submit.prevent="handleChangePasswordSubmit" class="space-y-3.5">
        <div>
          <label class="block text-xs font-semibold text-slate-700 mb-1">Cari (Köhnə) Şifrəniz</label>
          <input type="password" v-model="changePasswordForm.old_password" required placeholder="Hazırkı şifrəniz" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3.5 py-2.5 text-xs font-medium focus:ring-2 focus:ring-brand-500">
        </div>
        <div>
          <label class="block text-xs font-semibold text-slate-700 mb-1">Yeni Şifrəniz</label>
          <input type="password" v-model="changePasswordForm.new_password" required placeholder="Yeni şifrəniz" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3.5 py-2.5 text-xs font-medium focus:ring-2 focus:ring-brand-500">
        </div>
        <div>
          <label class="block text-xs font-semibold text-slate-700 mb-1">Yeni Şifrənin Təkrarı</label>
          <input type="password" v-model="changePasswordForm.confirm_password" required placeholder="Yeni şifrənizi təkrar yazın" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3.5 py-2.5 text-xs font-medium focus:ring-2 focus:ring-brand-500">
        </div>
        <div class="pt-2 flex gap-2">
          <button type="button" @click="showChangePasswordModal = false" class="flex-1 py-2.5 bg-slate-100 text-slate-600 rounded-xl text-xs font-bold">
            Ləğv et
          </button>
          <button type="submit" :disabled="isSubmitting" class="touch-btn flex-1 py-2.5 bg-brand-600 hover:bg-brand-700 text-white font-bold rounded-xl text-xs shadow-md">
            {{ isSubmitting ? 'Saxlanılır...' : 'Yadda Saxla' }}
          </button>
        </div>
      </form>
    </div>
  </div>

  <!-- Modal: Assign Classes for Teacher -->'''

assert old_modals_end in content, "old_modals_end not found"
content = content.replace(old_modals_end, new_modals, 1)

# 11. Vue Data: Add password fields
old_vue_data = '''        // Moderator Assignment Modal
        showAssignModeratorModal: false,
        targetSchoolForModerator: {},
        selectedModeratorUserId: '',
        schoolPotentialModerators: []'''

new_vue_data = '''        // Moderator Assignment Modal
        showAssignModeratorModal: false,
        targetSchoolForModerator: {},
        selectedModeratorUserId: '',
        schoolPotentialModerators: [],

        // Password Management
        showForgotPasswordModal: false,
        forgotTab: 'user',
        forgotUserForm: { username: '', contact_phone: '' },
        forgotAdminForm: { recovery_code: '', new_password: '', confirm_password: '' },

        showChangePasswordModal: false,
        changePasswordForm: { old_password: '', new_password: '', confirm_password: '' },

        adminPasswordResets: []'''

assert old_vue_data in content, "old_vue_data not found"
content = content.replace(old_vue_data, new_vue_data, 1)

# 12. Vue Methods: Add password methods and loadAdminPasswordResets
old_load_admin = '''      async loadAdminData() {
        await this.loadAdminOverview();
        await this.loadAdminPendingRequests();
        await this.loadAdminSchoolsSummary();
        await this.loadAdminTeachers();
        await this.loadAdminStudents();
        await this.loadAllClasses();
      },'''

new_load_admin = '''      async loadAdminData() {
        await this.loadAdminOverview();
        await this.loadAdminPendingRequests();
        await this.loadAdminPasswordResets();
        await this.loadAdminSchoolsSummary();
        await this.loadAdminTeachers();
        await this.loadAdminStudents();
        await this.loadAllClasses();
      },'''

assert old_load_admin in content, "old_load_admin not found"
content = content.replace(old_load_admin, new_load_admin, 1)

old_methods_anchor = '''      async approveUser(userId) {'''

new_methods_anchor = '''      async loadAdminPasswordResets() {
        try {
          const sId = this.currentUser && this.currentUser.is_moderator ? this.currentUser.school_id : this.selectedAdminSchoolId;
          const url = sId ? `/api/admin/password-resets?school_id=${sId}` : '/api/admin/password-resets';
          const res = await fetch(url, {
            headers: { 'X-User-Id': this.currentUser.id }
          });
          this.adminPasswordResets = await res.json();
        } catch(e) {}
      },

      openForgotPasswordModal() {
        this.showAuthModal = false;
        this.forgotTab = this.authRole === 'admin' ? 'admin' : 'user';
        this.forgotUserForm = { username: '', contact_phone: '' };
        this.forgotAdminForm = { recovery_code: '', new_password: '', confirm_password: '' };
        this.showForgotPasswordModal = true;
      },

      openChangePasswordModal() {
        this.changePasswordForm = { old_password: '', new_password: '', confirm_password: '' };
        this.showChangePasswordModal = true;
      },

      async handleForgotPasswordSubmit() {
        if (!this.forgotUserForm.username.trim()) {
          this.showToast('İstifadəçi adınızı qeyd edin!', 'error');
          return;
        }
        this.isSubmitting = true;
        try {
          const res = await fetch('/api/auth/forgot-password-request', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(this.forgotUserForm)
          });
          const d = await res.json();
          if (!res.ok) throw new Error(d.detail || 'Xəta baş verdi');
          this.showToast(d.message);
          this.showForgotPasswordModal = false;
        } catch(e) {
          this.showToast(e.message, 'error');
        } finally {
          this.isSubmitting = false;
        }
      },

      async handleAdminRecoverySubmit() {
        if (!this.forgotAdminForm.recovery_code.trim()) {
          this.showToast('Bərpa açar sözünü (kodu) daxil edin!', 'error');
          return;
        }
        if (this.forgotAdminForm.new_password !== this.forgotAdminForm.confirm_password) {
          this.showToast('Yeni şifrələr bir-biri ilə eyni deyil!', 'error');
          return;
        }
        if (this.forgotAdminForm.new_password.length < 3) {
          this.showToast('Şifrə ən azı 3 simvol olmalıdır!', 'error');
          return;
        }
        this.isSubmitting = true;
        try {
          const res = await fetch('/api/auth/admin-recovery-reset', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              recovery_code: this.forgotAdminForm.recovery_code,
              new_password: this.forgotAdminForm.new_password
            })
          });
          const d = await res.json();
          if (!res.ok) throw new Error(d.detail || 'Xəta baş verdi');
          this.showToast(d.message);
          this.showForgotPasswordModal = false;
          this.openAdminLogin();
        } catch(e) {
          this.showToast(e.message, 'error');
        } finally {
          this.isSubmitting = false;
        }
      },

      async handleChangePasswordSubmit() {
        if (!this.changePasswordForm.old_password.trim() || !this.changePasswordForm.new_password.trim()) {
          this.showToast('Bütün xanaları doldurun!', 'error');
          return;
        }
        if (this.changePasswordForm.new_password !== this.changePasswordForm.confirm_password) {
          this.showToast('Yeni şifrələr bir-biri ilə uyğun gəlmir!', 'error');
          return;
        }
        if (this.changePasswordForm.new_password.length < 3) {
          this.showToast('Yeni şifrə ən azı 3 simvol olmalıdır!', 'error');
          return;
        }
        this.isSubmitting = true;
        try {
          const res = await fetch('/api/auth/change-own-password', {
            method: 'POST',
            headers: { 
              'Content-Type': 'application/json',
              'X-User-Id': this.currentUser.id
            },
            body: JSON.stringify({
              old_password: this.changePasswordForm.old_password,
              new_password: this.changePasswordForm.new_password
            })
          });
          const d = await res.json();
          if (!res.ok) throw new Error(d.detail || 'Xəta baş verdi');
          this.showToast(d.message);
          this.showChangePasswordModal = false;
        } catch(e) {
          this.showToast(e.message, 'error');
        } finally {
          this.isSubmitting = false;
        }
      },

      async resolvePasswordReset(resetItem, customPassword = '') {
        const pwd = customPassword || prompt(`${resetItem.full_name} üçün yeni şifrə daxil edin:`, '123456');
        if (!pwd) return;
        try {
          const res = await fetch(`/api/admin/password-resets/${resetItem.id}/resolve`, {
            method: 'POST',
            headers: { 
              'Content-Type': 'application/json',
              'X-User-Id': this.currentUser.id
            },
            body: JSON.stringify({ new_password: pwd })
          });
          const d = await res.json();
          if (!res.ok) throw new Error(d.detail || 'Xəta baş verdi');
          this.showToast(d.message);
          await this.loadAdminData();
        } catch(e) {
          this.showToast(e.message, 'error');
        }
      },

      async approveUser(userId) {'''

assert old_methods_anchor in content, "old_methods_anchor not found"
content = content.replace(old_methods_anchor, new_methods_anchor, 1)

with open(index_path, "w", encoding="utf-8") as f:
    f.write(content)

print("SUCCESS: index.html fully updated!")
