import os

index_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "index.html")
with open(index_path, "r", encoding="utf-8") as f:
    text = f.read()

# Helper template generator for password input with show/hide toggle
def make_pw_field(key, v_model, placeholder, extra_classes="text-xs"):
    return f'''<div class="relative">
            <input :type="showPasswordMap['{key}'] ? 'text' : 'password'" v-model="{v_model}" required placeholder="{placeholder}" 
                   class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3.5 py-2.5 pr-10 {extra_classes} focus:ring-2 focus:ring-brand-500">
            <button type="button" @click="togglePassword('{key}')" tabindex="-1" title="Şifrəni göstər / gizlə"
                    class="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-slate-700 focus:outline-none">
              <svg v-if="!showPasswordMap['{key}']" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
              <svg v-else class="w-4 h-4 text-brand-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l18 18" />
              </svg>
            </button>
          </div>'''

# 1. Login Form Password
t_login = '''          <input type="password" v-model="loginForm.password" required placeholder="Şifrəniz" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3.5 py-2.5 text-sm focus:ring-2 focus:ring-brand-500">'''
r_login = make_pw_field("login", "loginForm.password", "Şifrəniz", "text-sm")
assert t_login in text, "t_login not found"
text = text.replace(t_login, r_login, 1)

# 2. Student Register Password
t_student = '''          <input type="password" v-model="studentRegForm.password" required placeholder="Şifrənizi təyin edin" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-xs">'''
r_student = make_pw_field("student_reg", "studentRegForm.password", "Şifrənizi təyin edin", "text-xs")
assert t_student in text, "t_student not found"
text = text.replace(t_student, r_student, 1)

# 3. Director Register Password
t_dir = '''          <input type="password" v-model="directorRegForm.password" required placeholder="Şifrənizi təyin edin" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-xs">'''
r_dir = make_pw_field("director_reg", "directorRegForm.password", "Şifrənizi təyin edin", "text-xs")
assert t_dir in text, "t_dir not found"
text = text.replace(t_dir, r_dir, 1)

# 4. Teacher Register Password
t_teacher = '''          <input type="password" v-model="teacherRegForm.password" required placeholder="Şifrəniz" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-xs">'''
r_teacher = make_pw_field("teacher_reg", "teacherRegForm.password", "Şifrəniz", "text-xs")
assert t_teacher in text, "t_teacher not found"
text = text.replace(t_teacher, r_teacher, 1)

# 5. Admin Recovery Passwords
t_admin_new = '''          <input type="password" v-model="forgotAdminForm.new_password" required placeholder="Yeni şifrəniz" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3.5 py-2.5 text-xs font-medium focus:ring-2 focus:ring-purple-500">'''
r_admin_new = make_pw_field("admin_rec_new", "forgotAdminForm.new_password", "Yeni şifrəniz", "text-xs font-medium focus:ring-purple-500")
assert t_admin_new in text, "t_admin_new not found"
text = text.replace(t_admin_new, r_admin_new, 1)

t_admin_conf = '''          <input type="password" v-model="forgotAdminForm.confirm_password" required placeholder="Yeni şifrəni təkrar yazın" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3.5 py-2.5 text-xs font-medium focus:ring-2 focus:ring-purple-500">'''
r_admin_conf = make_pw_field("admin_rec_conf", "forgotAdminForm.confirm_password", "Yeni şifrəni təkrar yazın", "text-xs font-medium focus:ring-purple-500")
assert t_admin_conf in text, "t_admin_conf not found"
text = text.replace(t_admin_conf, r_admin_conf, 1)

# 6. Change Password Modal Fields
t_chg_old = '''          <input type="password" v-model="changePasswordForm.old_password" required placeholder="Hazırkı şifrəniz" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3.5 py-2.5 text-xs font-medium focus:ring-2 focus:ring-brand-500">'''
r_chg_old = make_pw_field("chg_old", "changePasswordForm.old_password", "Hazırkı şifrəniz", "text-xs font-medium")
assert t_chg_old in text, "t_chg_old not found"
text = text.replace(t_chg_old, r_chg_old, 1)

t_chg_new = '''          <input type="password" v-model="changePasswordForm.new_password" required placeholder="Yeni şifrəniz" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3.5 py-2.5 text-xs font-medium focus:ring-2 focus:ring-brand-500">'''
r_chg_new = make_pw_field("chg_new", "changePasswordForm.new_password", "Yeni şifrəniz", "text-xs font-medium")
assert t_chg_new in text, "t_chg_new not found"
text = text.replace(t_chg_new, r_chg_new, 1)

t_chg_conf = '''          <input type="password" v-model="changePasswordForm.confirm_password" required placeholder="Yeni şifrənizi təkrar yazın" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3.5 py-2.5 text-xs font-medium focus:ring-2 focus:ring-brand-500">'''
r_chg_conf = make_pw_field("chg_conf", "changePasswordForm.confirm_password", "Yeni şifrənizi təkrar yazın", "text-xs font-medium")
assert t_chg_conf in text, "t_chg_conf not found"
text = text.replace(t_chg_conf, r_chg_conf, 1)

# 7. Add Vue data showPasswordMap
t_vdata = '''        changePasswordForm: { old_password: '', new_password: '', confirm_password: '' },'''
r_vdata = '''        changePasswordForm: { old_password: '', new_password: '', confirm_password: '' },
        showPasswordMap: {},'''
assert t_vdata in text, "t_vdata not found"
text = text.replace(t_vdata, r_vdata, 1)

# 8. Add Vue method togglePassword
t_vmethod = '''      openForgotPasswordModal() {'''
r_vmethod = '''      togglePassword(key) {
        this.showPasswordMap[key] = !this.showPasswordMap[key];
      },

      openForgotPasswordModal() {'''
assert t_vmethod in text, "t_vmethod not found"
text = text.replace(t_vmethod, r_vmethod, 1)

with open(index_path, "w", encoding="utf-8") as f:
    f.write(text)

print("SUCCESS: Password visibility toggles added to all forms!")
