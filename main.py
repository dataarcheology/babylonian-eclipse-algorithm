import json
from datetime import datetime, timedelta

class BabylonianEclipsePredictor:
    def __init__(self, start_date_str, initial_draconitic_phase):
        """
        Babil System B (Zigzag) Mantığı ile Tutulma Hesaplayıcı
        
        :param start_date_str: Başlangıç Syzygy (Yeni Ay) tarihi (YYYY-MM-DD)
        :param initial_draconitic_phase: Ay'ın düğüm noktasına uzaklığı (0.0 ile 1.0 arası)
                                         0.0 veya 0.5 = Tam Düğüm Noktası (Kesin Tutulma)
        """
        self.start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        self.draconitic_phase = initial_draconitic_phase
        
        # Babil Sabitleri (Sexagesimal sistemden ondalığa çevrilmiştir)
        self.SYNODIC_MONTH_DAYS = 29.530594  # Ortalama Yeni Ay süresi
        
        # Babil'in "Saros" Keşfi: 223 Synodic Ay ≈ 242 Draconitic Ay
        # Bu, her yeni ayda Draconitic fazın ne kadar ilerlediğini verir.
        # Bu oran System B tabletlerindeki "Zigzag" fonksiyonunun eğimidir.
        self.DRACONITIC_INCREMENT = (242.0 / 223.0) 

    def generate_ephemeris(self, num_months=1000, threshold=0.045):
        """
        Gelecek aylar için Babil usulü 'Tablet' verisi oluşturur.
        
        :param num_months: Hesaplanacak ay sayısı
        :param threshold: Tutulma eşiği (Düğüm noktasına ne kadar yakınsa o kadar riskli)
        :return: JSON formatına uygun liste
        """
        results = []
        current_date = self.start_date
        current_phase = self.draconitic_phase

        for i in range(num_months):
            # Fazın 0 ile 1 arasında kalmasını sağla (Modüler Aritmetik)
            normalized_phase = current_phase % 1.0
            
            # Düğüm Noktasına Uzaklık (0.0 veya 0.5 düğüm noktalarıdır)
            # Distance 0'a yaklaştıkça "Kuzey Düğümü", 0.5'e yaklaştıkça "Güney Düğümü"
            dist_to_node_1 = abs(normalized_phase - 0.0)
            dist_to_node_2 = abs(normalized_phase - 0.5)
            dist_to_node_3 = abs(normalized_phase - 1.0) # 0.99... durumu için
            
            min_dist = min(dist_to_node_1, dist_to_node_2, dist_to_node_3)
            
            is_eclipse_possible = min_dist < threshold
            
            entry = {
                "month_index": i,
                "date": current_date.strftime("%Y-%m-%d"),
                "draconitic_phase": round(normalized_phase, 5),
                "node_distance": round(min_dist, 5),
                "eclipse_prediction": "POSSIBLE" if is_eclipse_possible else "NO",
                "type": "N/A"
            }

            if is_eclipse_possible:
                # Babil tabletlerinde olduğu gibi 'Kuzey' veya 'Güney' tahmini
                if dist_to_node_2 < threshold:
                    entry["type"] = "South Node Eclipse (Descending)"
                else:
                    entry["type"] = "North Node Eclipse (Ascending)"
                
                results.append(entry)

            # Bir sonraki aya (satıra) geçiş - Babil 'Step' işlemi
            current_date += timedelta(days=self.SYNODIC_MONTH_DAYS)
            current_phase += self.DRACONITIC_INCREMENT

        return results

# --- KULLANIM ÖRNEĞİ (Bunu main.py olarak çalıştırabilirsin) ---

# Referans: 11 Ocak 2024 Yeni Ay'ı (Bu tarihte Ay düğüme yakındı ama tam üstünde değildi)
# Fazı deneme yanılma veya modern efemeristen alıp buraya 'seed' (tohum) olarak giriyoruz.
# 0.48 diyelim (Güney düğümüne çok yakın)

predictor = BabylonianEclipsePredictor(start_date_str="2024-01-11", initial_draconitic_phase=0.48)
babylonian_data = predictor.generate_ephemeris(num_months=2400) # Yaklaşık 200 yıllık veri

# Veriyi GitHub için JSON olarak kaydet
with open("babylonian_eclipse_data.json", "w", encoding="utf-8") as f:
    json.dump(babylonian_data, f, indent=4)

print(f"{len(babylonian_data)} adet potansiyel tutulma bulundu ve JSON'a yazıldı.")
