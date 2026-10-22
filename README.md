# Məktəb 31 - Sumqayıt | Elektron Məktəb və Jurnal Sistemi

Sumqayıt şəhər 31 nömrəli tam orta məktəb üçün hazırlanmış müasir, çoxfunksiyalı elektron idarəetmə və jurnal platforması.

---

## 🌟 Əsas Funksiyalar

1. **Hər Müəllimə Şəxsi Elektron Jurnal:**
   - Müəllim yalnız özünün tədris etdiyi sinifləri və fənləri görür.
   - **Davamiyyət:** Tək toxunuşla "Q (İştirak)", "Q/B (Qaib)", "S (Səbəbli)" statuslarının qeyd olunması.
   - **Qiymətləndirmə:** Gündəlik formativ qiymətlər, KSQ-1, KSQ-2, KSQ-3 və BSQ ballarının daxil edilməsi və silinməsi.
   - **Mövzu və Ev Tapşırıqları:** Keçirilən dərsin mövzusunun və ev tapşırığının qeyd edilməsi (şagirdlər dərhal görür).

2. **Şagird və Valideyn Bölməsi (Açıq Baxış):**
   - Sinif seçərək həmin sinifdə dərs deyən müəllimlərə baxış.
   - Fənlər üzrə verilmiş ev tapşırıqları və keçirilən mövzuların gündəliyi.

3. **Məktəb İnzibatçısı (Direktor / Admin Paneli):**
   - Yeni müəllim əlavə etmək və şifrə təyin etmək.
   - Müəllimə istənilən fənn və sinif təhkim etmək.
   - Yeni siniflər açmaq və şagirdləri siniflərə əlavə etmək.
   - Məktəbin ümumi davamiyyət göstəricilərini canlı izləmək.

4. **Bütün Cihazlarda Dəstək (PWA & Mobil Uyğunluq):**
   - Kompüter, planşet, iPhone və Android telefonlarda ideal görünüş.
   - Telefonda brauzer menyusundan **"Ekrana əlavə et" (və ya "Tətbiqi Quraşdır")** seçdikdə birbaşa telefon proqramı kimi quraşdırılır.

---

## 🚀 Kompüterdə İşə Salmaq

### Ən Sadə Yol:
`start_app.bat` faylına iki dəfə klikləyin. Server avtomatik başlayacaq və tətbiq pəncərəsi açılacaq.

### Və ya Əmr Sətri ilə:
```bash
python server.py
```
* **Kompüterdə daxil olmaq üçün:** `http://localhost:8000`
* **Telefonda açmaq üçün:** Kompüter və telefon eyni Wi-Fi şəbəkəsinə qoşulubsa, terminalda görünən yerli IP ünvanı (məsələn: `http://192.168.1.5:8000`) telefonun brauzerində yazın.

---

## 🌐 Bütün Məktəb Üçün Replit-də 24/7 Yayımlamaq (Onlayn Link)

Bu layihəni Replit-də onlayn etmək çox asandır:
1. [Replit.com](https://replit.com)-a daxil olun.
2. **"Create Repl"** düyməsini sıxın və şablon olaraq **"Python"** və ya **"FastAPI"** seçin.
3. Bu layihədəki faylları (`server.py`, `requirements.txt`, `static/` qovluğunu) Repl-ə sürükləyib atın (drag & drop).
4. **"Run"** düyməsinə klikləyin.
5. Replit sizə `https://sizinyeniad.replit.app` kimi daimi onlayn link verəcək. Həmin linki bütün müəllimlər və şagirdlər həm telefonlarında, həm kompüterlərində 24/7 aça biləcəklər!

---

## 🔑 Hazır Sınaq Giriş Hesabları

| Rol | İstifadəçi Adı | Şifrə | Təsvir |
|---|---|---|---|
| **Müəllim** | `esma` | `3131` | Mirzəliyeva Əsma (İnformatika) |
| **Müəllim** | `sevinc` | `1234` | Əliyeva Sevinc (Azərbaycan dili) |
| **Müəllim** | `reshad` | `1234` | Məmmədov Rəşad (Tarix) |
| **Müəllim** | `gunel` | `1234` | Həsənova Günel (İngilis dili) |
| **Müəllim** | `vusal` | `1234` | Qasımov Vüsal (Riyaziyyat) |
| **İnzibatçı** | `admin` | `admin31` | Məktəb Rəhbərliyi / Direktor |

---
**Müəllif:** Sumqayıt şəhər 31 nömrəli tam orta məktəb. Mirzəliyeva Əsma.
