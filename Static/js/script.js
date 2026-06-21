document.addEventListener('DOMContentLoaded', () => {
    const barlar = document.querySelectorAll('.bar-ic');

    // Sayfa açıldıktan yarım saniye sonra animasyonu başlat (Garanti olsun)
    setTimeout(() => {
        barlar.forEach(bar => {
            // data-width içine sakladığımız gerçek oranı alıyoruz (%32 gibi)
            const gercekOran = bar.getAttribute('data-width');
            
            // Şimdi genişliği veriyoruz, CSS transition bunu kaydırarak yapacak
            bar.style.width = gercekOran;
        });
    }, 500); 
});