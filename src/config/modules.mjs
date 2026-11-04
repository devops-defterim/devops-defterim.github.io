// Menü sırası ve grupları burada yönetilir.
// Yeni modül eklemek: src/content/docs/<dir>/ klasörünü oluştur ve bu listeye bir girdi ekle.
// Sayfaların modül içindeki sırası frontmatter'daki `order` alanından gelir.
// Alt klasörler menüde grup olur; grup adı `groups` içinden okunur.
// `sidebar: false` olan modül menüde ve ana sayfadaki listede görünmez.
// Tek bir sayfayı menüden gizlemek için o sayfanın frontmatter'ına `sidebar: { hidden: true }` yazılır.
export const modules = [
	{
		dir: 'baslangic',
		label: 'Gerekli Kurulumlar',
		summary: 'Derslerde kullanılan AWS çalışma makinesinin açılması.',
	},
	{
		dir: 'linux',
		label: 'Linux',
		summary: 'Shell, dosyalar ve izinler, kullanıcılar, process yönetimi, scripting, loglama, disk ve network.',
		groups: { 'shell-scripting': 'Shell scripting' },
	},
	{
		dir: 'git',
		label: 'Git ve GitHub',
		summary: 'Versiyon kontrolü, branch yönetimi ve GitHub ile çalışma.',
	},
	{
		dir: 'mini-proje',
		label: 'Mini Proje: Linux, Git ve GitHub',
		summary: 'Linux ve Git konularını bir sunucu kurulumunda bir araya getiren proje.',
	},
	{
		dir: 'bulut-temelleri',
		label: 'Bulut Bilişim Temelleri',
		summary: 'Sanallaştırmadan buluta, servis modelleri, yazılım geliştirme döngüsü ve DevOps.',
	},
	{
		dir: 'aws',
		label: 'AWS',
		summary: 'IAM, AWS CLI, S3, EC2 ve EBS.',
		groups: { iam: 'IAM', s3: 'S3', ec2: 'EC2', 'ebs-ve-ami': 'EBS ve AMI' },
	},
];
