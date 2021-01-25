class AwsAllowlister < Formula
  include Language::Python::Virtualenv

  desc "Shiny new formula"
  homepage "https://github.com/salesforce/aws-allowlister"
  url "https://files.pythonhosted.org/packages/86/62/ccc24158e8b7115e7ae0510bbf640a30bb36b42028f9bfff481bac6e4df1/aws-allowlister-0.0.4.tar.gz"
  sha256 "170946395a30dca47ab1cd1c6a781fa31352da9b0360cfbae6c6d465056716a4"

  depends_on "python3"

  resource "beautifulsoup4" do
    url "https://files.pythonhosted.org/packages/6b/c3/d31704ae558dcca862e4ee8e8388f357af6c9d9acb0cad4ba0fbbd350d9a/beautifulsoup4-4.9.3.tar.gz"
    sha256 "84729e322ad1d5b4d25f805bfa05b902dd96450f43842c4e99067d5e1369eb25"
  end

  resource "certifi" do
    url "https://files.pythonhosted.org/packages/06/a9/cd1fd8ee13f73a4d4f491ee219deeeae20afefa914dfb4c130cfc9dc397a/certifi-2020.12.5.tar.gz"
    sha256 "1a4995114262bffbc2413b159f2a1a480c969de6e6eb13ee966d470af86af59c"
  end

  resource "chardet" do
    url "https://files.pythonhosted.org/packages/ee/2d/9cdc2b527e127b4c9db64b86647d567985940ac3698eeabc7ffaccb4ea61/chardet-4.0.0.tar.gz"
    sha256 "0d6f53a15db4120f2b08c94f11e7d93d2c911ee118b6b30a04ec3ee8310179fa"
  end

  resource "click" do
    url "https://files.pythonhosted.org/packages/27/6f/be940c8b1f1d69daceeb0032fee6c34d7bd70e3e649ccac0951500b4720e/click-7.1.2.tar.gz"
    sha256 "d2b5255c7c6349bc1bd1e59e08cd12acbbd63ce649f2588755783aa94dfb6b1a"
  end

  resource "contextlib2" do
    url "https://files.pythonhosted.org/packages/02/54/669207eb72e3d8ae8b38aa1f0703ee87a0e9f88f30d3c0a47bebdb6de242/contextlib2-0.6.0.post1.tar.gz"
    sha256 "01f490098c18b19d2bd5bb5dc445b2054d2fa97f09a4280ba2c5f3c394c8162e"
  end

  resource "idna" do
    url "https://files.pythonhosted.org/packages/ea/b7/e0e3c1c467636186c39925827be42f16fee389dc404ac29e930e9136be70/idna-2.10.tar.gz"
    sha256 "b307872f855b18632ce0c21c5e45be78c0ea7ae4c15c828c20788b26921eb3f6"
  end

  resource "policy-sentry" do
    url "https://files.pythonhosted.org/packages/2b/89/104444db0d43dd91f17862d9a928d3f7be65fa092c572fe6f512f084f245/policy_sentry-0.11.3.tar.gz"
    sha256 "652137d702c5cb8fbd1e1657fbbea931eb38e5fc64def876e47cd02cc76b7530"
  end

  resource "PyYAML" do
    url "https://files.pythonhosted.org/packages/a0/a4/d63f2d7597e1a4b55aa3b4d6c5b029991d3b824b5bd331af8d4ab1ed687d/PyYAML-5.4.1.tar.gz"
    sha256 "607774cbba28732bfa802b54baa7484215f530991055bb562efbed5b2f20a45e"
  end

  resource "requests" do
    url "https://files.pythonhosted.org/packages/6b/47/c14abc08432ab22dc18b9892252efaf005ab44066de871e72a38d6af464b/requests-2.25.1.tar.gz"
    sha256 "27973dd4a904a4f13b263a19c866c13b92a39ed1c964655f025f3f8d3d75b804"
  end

  resource "schema" do
    url "https://files.pythonhosted.org/packages/0d/de/84afc54d41aea9787c6d8814391a2d296a8240eef5b59d11704a82d82064/schema-0.7.2.tar.gz"
    sha256 "b536f2375b49fdf56f36279addae98bd86a8afbd58b3c32ce363c464bed5fc1c"
  end

  resource "soupsieve" do
    url "https://files.pythonhosted.org/packages/58/5d/445e21e92345848305eecf473338e9ec7ed8905b99ea78415042060127fc/soupsieve-2.1.tar.gz"
    sha256 "6dc52924dc0bc710a5d16794e6b3480b2c7c08b07729505feab2b2c16661ff6e"
  end

  resource "SQLAlchemy" do
    url "https://files.pythonhosted.org/packages/b7/10/b6d02efa2cb10dca0671fd62c9091c1e49831b266658fd7a056c577621cb/SQLAlchemy-1.3.22.tar.gz"
    sha256 "758fc8c4d6c0336e617f9f6919f9daea3ab6bb9b07005eda9a1a682e24a6cacc"
  end

  resource "urllib3" do
    url "https://files.pythonhosted.org/packages/29/e6/d1a1d78c439cad688757b70f26c50a53332167c364edb0134cadd280e234/urllib3-1.26.2.tar.gz"
    sha256 "19188f96923873c92ccb987120ec4acaa12f0461fa9ce5d3d0772bc965a39e08"
  end

  def install
    virtualenv_create(libexec, "python3")
    virtualenv_install_with_resources
  end

  test do
    false
  end
end
