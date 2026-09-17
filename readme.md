### llm service

Bu proje basit bir iş görecek. Aslında 17 Eylül toplantısında "bir LLM servimiz olsa token kullanımı ve energy gibi metrikleri izleyebilir miyiz " sorusu üzerine basit bir örnek olarak aklıma takıldı.
Zaten ollama run modelismi --verbose yaptığımızda lokalimizde kullandığımız token vb. gözüküyor.

Fakat biz LLM'i kendi sunucumuzda host ettiğimiz bir senaryoda vLLM gibi şeyler öğrenmemiz gerekebilir. Bu kısımda çok bilgim yok sonra bakmam gerekecek.

Ama mantık basit, cliennt'de bir istek server'a gelecek. Server'da llm çalışacak ve üstteki metrikleri de toplayıp kullanıcı tarafında (panelde) gösterecek. Hatta nvidi-smi ile enerji tüketimini de gösterebiliriz. 

Bu nedenle bu uygulama başladı.


Verisyonlama : 

v0 - v0.8 : LLM'e request atıp response alabildiğimiz bir servis oldu. Şu anda düz HTTP mantığında çalışıyor. Maalesef server tarafını uzak sununucuda serve edemedim. Droplet'te ram ve cpu tüketimi fırlayınca durdurdum. Lokalde de windows'ta vllm sorun çıkarıyor gibiydi. Bu nedenle server tarafını doğreudan vllm kaldırıp basit tuttum. 

v0.9 - v1.0: Nihai istediğimiz yer, enerji tüketimi için bir sınıf yazdırdım claude'a. Hem anlık ortamala ne kadar güç tüketiyor onu görüyoruz, hem de toplamda ne kadar elektrik harcandığını görüyoruz hem de TL bazında ne kadar fiyat tuttuğunu görüyoruz. Diğer güzel kısım da toplamı da sol tarafta ekliyoruz.   
