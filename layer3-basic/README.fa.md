# لایه ۳: SSH پایه - ساده‌ترین روش

> **⭐ آسان‌ترین روش برای شروع**
> پورت 22 - مناسب تست و یادگیری

[← بازگشت به راهنمای اصلی](../README.fa.md)

---

## این روش چیست؟

ساده‌ترین روش پراکسی که از SSH استاندارد روی پورت 22 استفاده می‌کند.

**مزایا:**
- نصب بسیار آسان (5 دقیقه)
- بدون نیاز به تنظیمات پیچیده
- رمزنگاری SSH استاندارد

**محدودیت:**
- پورت 22 در برخی شبکه‌ها ممکن است فیلتر باشد
- برای سانسور سخت مناسب نیست

---

--------------------------------------------------
مرحله ۱: خرید سرور VPS
--------------------------------------------------

**اگر از قبل سرور لینوکس با Ubuntu دارید، این مرحله را رد کنید و به مرحله ۲ بروید.**

**برای خرید از IONOS (پیشنهادی):** [راهنمای خرید سرور از IONOS](../buy-ionos-server.fa.md)

### نکات خرید:
- سیستم‌عامل: **Ubuntu**
- پلن ارزان کافی است
- لوکیشن به انتخاب شما

**اطلاعات مورد نیاز از سرور:**
- IP سرور
- نام کاربری: root
- رمز عبور

---

--------------------------------------------------
مرحله ۲: اتصال SSH
--------------------------------------------------

**[راهنمای اتصال به سرور با SSH](../ssh-connection.fa.md)**

خلاصه:
```bash
ssh root@SERVER-IP
```

---

--------------------------------------------------
مرحله ۳: نصب لایه ۳
--------------------------------------------------

این دستور را اجرا کنید:

```bash
curl -fsSL https://raw.githubusercontent.com/myotgo/Proxy/main/layer3-basic/install.sh -o install.sh && bash install.sh
```
then go to the given url to manage user and ...
https://87.106.68.203:8443
https://server-IP:8443
<img width="1023" height="616" alt="Screenshot 2026-01-30 at 19 14 59" src="https://github.com/user-attachments/assets/e25477b7-20e0-44d8-9359-7259de2d8ed9" />


then you will see a warning that is because we use self sign certificate to create https panel

click on advance
<img width="1913" height="1011" alt="1" src="https://github.com/user-attachments/assets/4a18b53a-eaaa-4e51-b9c7-d21812eb855e" />

then click on Proceed to IP (unsafe)
as we are using a fake SSL (we dont want to pay for SSL so we use a fake one to have https insteed of http) browser find this site is not valid in their sertificate list
<img width="1918" height="1012" alt="2" src="https://github.com/user-attachments/assets/4f763fcc-5bb8-4c0a-b96f-e09285652788" />

after that you will see this page(login). you can change the language to persian if you want
insert username and password of the server(the one from IONOS)

<img width="2537" height="1393" alt="Screenshot 2026-01-30 at 19 34 00" src="https://github.com/user-attachments/assets/30ac2bde-59bc-4379-af1d-5c8846485210" />

this is the management panel
you can add and delete user from here
<img width="2559" height="1410" alt="Screenshot 2026-01-30 at 19 36 25" src="https://github.com/user-attachments/assets/5262345c-7f4d-47d4-bc38-34dff8dd7111" />

you can use different methods here for different layers
but except the first 3 layer, other do not work in iran at the moment
so it is better to use the first 1 as it seems it works better for iranian
<img width="2559" height="1410" alt="Screenshot 2026-01-30 at 19 38 11" src="https://github.com/user-attachments/assets/33037acb-db2d-442b-b1e0-eef5177ed1d1" />



or alternatively, you can use these urls to add or delete users






نصب خودکار انجام می‌شود.

---

--------------------------------------------------
مرحله ۴: اضافه کردن کاربر
--------------------------------------------------

برای هر نفر یک کاربر بسازید:

```bash
curl -fsSL https://raw.githubusercontent.com/myotgo/Proxy/main/common/add-user.sh -o add-user.sh && bash add-user.sh
```

نام کاربری و رمز عبور را وارد کنید.

---

--------------------------------------------------
مرحله ۵: مانیتورینگ کاربران
--------------------------------------------------

برای مشاهده کاربران متصل و وضعیت سرور:

```bash
curl -fsSL https://raw.githubusercontent.com/myotgo/Proxy/main/common/view-users.sh -o view-users.sh && bash view-users.sh
```

---

--------------------------------------------------
مرحله ۶: حذف کاربر (در صورت نیاز)
--------------------------------------------------

```bash
curl -fsSL https://raw.githubusercontent.com/myotgo/Proxy/main/common/delete-user.sh -o delete-user.sh && bash delete-user.sh username
```

---

## استفاده در iOS (NPV Tunnel)

### مرحله ۱: نصب اپلیکیشن

وارد App Store شوید و جستجو کنید:
**NPV Tunnel**

![NPV App Store](https://github.com/user-attachments/assets/22d012dd-eea8-4bde-9146-3a0e52154a88)

---

### مرحله ۲: ورود به Config

![Config Tab](https://github.com/user-attachments/assets/2497ee34-fcb2-4575-9e42-2b930b8d0b8d)

---

### مرحله ۳: اضافه کردن تنظیمات

روی **+** کلیک کنید.

![Add Config](https://github.com/user-attachments/assets/a9b01bb9-f03d-4d5e-bcf7-d920b44660a4)

**Add Config Manually** را انتخاب کنید.

![Add Manually](https://github.com/user-attachments/assets/b87227d4-5b41-443f-8707-2a322d2c018f)

---

### مرحله ۴: انتخاب SSH Config

![SSH Config](https://github.com/user-attachments/assets/ac804061-e32d-423a-8387-69d25e326e27)

---

### مرحله ۵: وارد کردن اطلاعات

اطلاعات را وارد کنید:
- SSH Host: IP سرور
- Port: **22**
- Username: نام کاربری شما
- Password: رمز عبور شما

![Fill SSH Info](https://github.com/user-attachments/assets/b232e341-4d59-4f2b-804d-d923f31a03e6)

روی **Save** کلیک کنید و سپس **Connect**.

✅ اتصال برقرار شد!

---

## استفاده در Android (Net Mod)

قدم به قدم:

![Android Step 1](https://github.com/user-attachments/assets/72e7e385-83cf-4139-98df-4d41a5097916)

![Android Step 2](https://github.com/user-attachments/assets/c308415b-1484-448d-8c9d-69c5c97aab2d)

![Android Step 3](https://github.com/user-attachments/assets/86f3cea3-3d09-48bd-93f0-7824ffa10cb1)

![Android Step 4](https://github.com/user-attachments/assets/9062ea58-d7bc-400c-92bb-0b00a830757a)

![Android Step 5](https://github.com/user-attachments/assets/2847c64f-7061-4860-96b8-c131cc672031)

**تنظیمات Android:**
- Host: IP سرور
- Port: **22**
- Username: نام کاربری
- Password: رمز عبور

---

## نکات مهم

- پورت 22 در برخی شبکه‌ها ممکن است فیلتر شود
- برای استفاده روزمره لایه ۴ (Nginx) بهتر است
- این روش برای یادگیری و تست عالی است

---
