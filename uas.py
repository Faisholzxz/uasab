#Nama   : Muhammad Faishol Fadhlurrohman Pratama
#NIM    : 191011402518
#Kelas  : 06TPLE025 

#Fuzzy Sugeno
#Studi Kasus : Oven

#Kematangan daging : min 8 menit dan max 12 menit.
#Banyaknya daging  : sedikit 40 dan banyak 80.
#Tingkat Kematangan  : rare 40, medium 50, dan welldone 60.

def down(x, xmin, xmax):
    return (xmax- x) / (xmax - xmin)

def up(x, xmin, xmax):
    return (x - xmin) / (xmax - xmin)

class Daging():
    minimum = 40
    maximum = 80

    def sedikit(self, x):
        if x >= self.maximum:
            return 0
        elif x <= self.minimum:
            return 1
        else:
            return down(x, self.minimum, self.maximum)

    def banyak(self, x):
        if x <= self.minimum:
            return 0
        elif x >= self.maximum:
            return 1
        else:
            return up(x, self.minimum, self.maximum)

class kematangan():
    minimum = 40
    medium = 50
    maximum = 60

    def rendah(self, x):
        if x >= self.medium:
            return 0
        elif x <= self.minimum:
            return 1
        else:
            return down(x, self.minimum, self.medium)
    
    def sedang(self, x):
        if self.minimum < x < self.medium:
            return up(x, self.minimum, self.medium)
        elif self.medium < x < self.maximum:
            return down(x, self.medium, self.maximum)
        elif x == self.medium:
            return 1
        else:
            return 0

    def tinggi(self, x):
        if x <= self.medium:
            return 0
        elif x >= self.maximum:
            return 1
        else:
            return up(x, self.medium, self.maximum)

class waktupanggang():
    minimum = 8
    maximum = 12
    
    def lambat(self, α):
        if α >= self.maximum:
            return 0
        elif α <= self.minimum:
            return 1

    def cepat(self, α):
        if α <= self.minimum:
            return 0
        elif α >= self.maximum:
            return 1

    # 2 permintaan 3 persediaan
    def inferensi(self, jumlah_Daging, jumlah_kematangan):
        pak = Daging()
        ktr = kematangan()
        result = []
       
        # [R1] Jika Daging SEDIKIT, dan kematangan RENDAH, 
        #     MAKA Putaran = 500
        α1 = min(pak.sedikit(jumlah_Daging), ktr.rendah(jumlah_kematangan))
        z1 = self.minimum
        result.append((α1, z1))

        # [R2] Jika Daging SEDIKIT, dan kematangan SEDANG, 
        #     MAKA Putaran = 10 * jumlah_kematangan + 100
        α2 = min(pak.sedikit(jumlah_Daging), ktr.sedang(jumlah_kematangan))
        z2 = 10 * jumlah_kematangan + 100
        result.append((α2, z2))

        # [R3] Jika Daging SEDIKIT, dan kematangan TINGGI, 
        #     MAKA Putaran = 10 * jumlah_kematangan + 200
        α3 = min(pak.sedikit(jumlah_Daging), ktr.tinggi(jumlah_kematangan))
        z3 = 10 * jumlah_kematangan + 200
        result.append((α3, z3))

        # [R4] Jika Daging BANYAK, dan kematangan RENDAH,
        #     MAKA Putaran = 5 * jumlah_Daging + 2 * jumlah_kematangan
        α4 = min(pak.banyak(jumlah_Daging), ktr.rendah(jumlah_kematangan))
        z4 = 5 * jumlah_Daging + 2 * jumlah_kematangan
        result.append((α4, z4))

        # [R5] Jika Daging BANYAK, dan kematangan SEDANG,
        #     MAKA Putaran = 5 * jumlah_Daging + 4 * jumlah_kematangan + 100
        α5 = min(pak.banyak(jumlah_Daging), ktr.sedang(jumlah_kematangan))
        z5 = 5 * jumlah_Daging + 4 * jumlah_kematangan + 100
        result.append((α5, z5))

        # [R6] Jika Daging BANYAK, dan kematangan TINGGI,
        #     MAKA Putaran = 5 * jumlah_Daging + 5 * jumlah_kematangan + 300
        α6 = min(pak.banyak(jumlah_Daging), ktr.tinggi(jumlah_kematangan))
        z6 = 5 * jumlah_Daging + 5 * jumlah_kematangan + 300
        result.append((α6, z6))

        return result
    
    def defuzifikasi(self, jumlah_Daging, jumlah_kematangan):
        inferensi_values = self.inferensi(jumlah_Daging, jumlah_kematangan)
        return sum([(value[0]* value[1]) for value in inferensi_values]) / sum([value[0] for value in inferensi_values])