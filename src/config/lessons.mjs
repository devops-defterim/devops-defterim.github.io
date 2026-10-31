// Ders numarası → video başlığı. Sayfaların meta satırında kullanılır.
export const lessons = {
	0: 'Açılış, Tanışma',
	1: "Gerekli Kurulumlar ve Linux'a Giriş",
	2: 'Linux Shell Kullanımı ve Temel Komutlar',
	3: 'Linux Klasör Yapısı, Dosya Manipülasyonu ve İzinler',
	4: 'Linux Kullanıcı Yönetimi',
	5: 'Linux Uygulama Yönetimi ve Boot',
	6: 'Linux Shell Scripting',
	7: 'Linux Shell Scripting',
	8: 'Linux İzleme, Loglama ve Disk Yönetimi',
	9: 'Linux Network ve Git',
	10: 'Git',
	11: 'Git',
	12: 'Git',
	13: 'Git',
	talimat: 'Linux, Git ve GitHub Mini Proje Talimatlar',
	14: 'Linux, Git ve GitHub Mini Proje Çözümü',
	15: 'Linux, Git ve GitHub Mini Proje Çözümü',
	16: 'Bulut Bilişim Tarihi ve Önemli Konseptler',
	17: 'Bulut Bilişim Tarihi ve Önemli Konseptler',
	18: 'AWS Temelleri',
	19: 'AWS IAM',
	20: 'AWS IAM ve CLI',
	21: 'S3',
	22: 'S3',
	23: 'S3',
	24: 'EC2',
	25: 'EC2',
	26: 'EC2 EBS',
	27: 'Temel Network',
	28: 'Temel Network',
};

export function lessonLabel(key) {
	return key === 'talimat' ? 'Mini proje talimat videosu' : `Ders ${key}`;
}
