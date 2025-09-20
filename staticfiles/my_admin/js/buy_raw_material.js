function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.open-submodel-modal').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            e.preventDefault();

            const mainId = this.dataset.mainId;

            fetch(`/admin/warehousing/rawmaterial/add-submodel/${mainId}/`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
                .then(response => {
                    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                    return response.text();
                })
                .then(html => {
                    let oldModal = document.getElementById('submodel-modal');
                    if (oldModal) oldModal.remove();

                    let modal = document.createElement('div');
                    modal.id = 'submodel-modal';
                    Object.assign(modal.style, {
                        position: 'fixed',
                        top: '50%',
                        left: '50%',
                        transform: 'translate(-50%, -50%)',
                        backgroundColor: 'white',
                        border: '1px solid #ccc',
                        padding: '20px',
                        zIndex: 100000,
                        maxWidth: '80vw',
                        maxHeight: '70vh',
                        overflowY: 'auto',
                        boxShadow: '0 4px 8px rgba(0,0,0,0.2)'
                    });
                    modal.innerHTML = html;

                    let closeBtn = document.createElement('button');
                    closeBtn.innerText = 'بستن';
                    closeBtn.style.marginTop = '10px';
                    closeBtn.addEventListener('click', () => {
                        modal.remove();
                    });
                    modal.appendChild(closeBtn);

                    document.body.appendChild(modal);

                    const form = modal.querySelector('#submodel-form');
                    if (!form) {
                        alert('فرم پیدا نشد!');
                        return;
                    }

                    form.addEventListener('submit', function (event) {
                        event.preventDefault();
                        const data = new FormData(form);
                        fetch(form.action || window.location.href, {
                            method: 'POST',
                            body: data,
                            headers: {
                                'X-Requested-With': 'XMLHttpRequest',
                                'X-CSRFToken': csrftoken,
                            },
                        })
                            .then(response => {
                                if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                                return response.json();
                            })
                            .then(data => {
                                if (data.success) {
                                    alert('ثبت با موفقیت انجام شد.');
                                    modal.remove();
                                    location.reload();
                                } else {
                                    let errorText = '';
                                    for (const [field, errors] of Object.entries(data.errors)) {
                                        errorText += `${field}: ${errors.join(', ')}\n`;
                                    }
                                    alert('خطا در ثبت:\n' + errorText);
                                }
                            })
                            .catch(err => {
                                alert('خطا در ارسال اطلاعات به سرور: ' + err.message);
                            });
                    });
                })
                .catch(err => {
                    alert('خطا در دریافت فرم از سرور: ' + err.message);
                });
        });
    });
});
