### llm service

Bu proje basit bir iş görecek. Aslında 17 Eylül toplantısında "bir LLM servimiz olsa token kullanımı ve energy gibi metrikleri izleyebilir miyiz " sorusu üzerine basit bir örnek olarak aklıma takıldı.
Zaten ollama run modelismi --verbose yaptığımızda lokalimizde kullandığımız token vb. gözüküyor.

Fakat biz LLM'i kendi sunucumuzda host ettiğimiz bir senaryoda vLLM gibi şeyler öğrenmemiz gerekebilir. Bu kısımda çok bilgim yok sonra bakmam gerekecek.

Ama mantık basit, cliennt'de bir istek server'a gelecek. Server'da llm çalışacak ve üstteki metrikleri de toplayıp kullanıcı tarafında (panelde) gösterecek. Hatta nvidi-smi ile enerji tüketimini de gösterebiliriz. 

Bu nedenle bu uygulama başladı.