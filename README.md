pydqximg
========
ドラクエ10の冒険者の広場画像の一括ダウンロード

### インストール (Windows)
* Python2.7 (http://www.python.org/download/)
* Setuptools (https://pypi.python.org/pypi/setuptools)
```
setuptools-0.<x>.win32-py2.7.exe
```
* Mechanize
```
Proxyが必要な場合は、以下を先に入力
> set https_proxy=あなたのproxy:ポート番号
> c:\python27\scripts\easy_install.exe mechanize
```
* BeautifulSoup4
```
> c:\python27\scripts\easy_install.exe beautifulsoup4
```
* imagesという名前のサブディレクトリを作成

### セットアップ
*  以下を記載したファイルを作成します。
```
1行目: ユーザ名
2行目: キャラクタID
  → 冒険日誌等をクリックした先のURLに含まれる番号
     例: http://hiroba.dqx.jp/sc/diary/XX/ のXX
3行目: 保存先ディレクトリ名

例：
user123
12345678901
images
```

### 実行
```
> c:\python27\python.exe pydqximg.py <上記ファイル名> <ワンタイムパス(あれば)>
```
* パスワードを聞かれたら入れます。
* 同じ名前のファイルが存在する場合、そのファイルはスキップします。
