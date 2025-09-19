function gregorian_to_jalali(gy, gm, gd) {
    var g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334];
    var jy = (gy <= 1600) ? 0 : 979;
    gy -= (gy <= 1600) ? 621 : 1600;
    var gy2 = (gm > 2) ? (gy + 1) : gy;
    var days = (365 * gy) + Math.floor((gy2 + 3) / 4) - Math.floor((gy2 + 99) / 100) +
        Math.floor((gy2 + 399) / 400) - 80 + gd + g_d_m[gm - 1];
    jy += 33 * Math.floor(days / 12053);
    days %= 12053;
    jy += 4 * Math.floor(days / 1461);
    days %= 1461;
    if (days > 365) {
        jy += Math.floor((days - 1) / 365);
        days = (days - 1) % 365;
    }
    var jm, jd;
    var jalali_days = [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29];
    for (var i = 0; i < 12 && days >= jalali_days[i]; i++) {
        days -= jalali_days[i];
    }
    jm = i + 1;
    jd = days + 1;
    return [jy, jm, jd];
}

function updateClock() {
    const now = new Date();
    const gy = now.getFullYear();
    const gm = now.getMonth() + 1;
    const gd = now.getDate();
    const [jy, jm, jd] = gregorian_to_jalali(gy, gm, gd);

    const hours = now.getHours().toString().padStart(2, '0');
    const minutes = now.getMinutes().toString().padStart(2, '0');
    const seconds = now.getSeconds().toString().padStart(2, '0');

    const dateString = `${jy}/${jm.toString().padStart(2, '0')}/${jd.toString().padStart(2, '0')}`;
    const timeString = `${hours}:${minutes}:${seconds}`;

    const dateEl = document.getElementById('date-part');
    const timeEl = document.getElementById('time-part');

    if (dateEl && timeEl) {
        dateEl.textContent = dateString;
        timeEl.textContent = timeString;
    }
}

document.addEventListener("DOMContentLoaded", function () {
    updateClock();
    setInterval(updateClock, 1000);
});