# Coin Tracker
pip install -r requirements.txt

## References
* https://pynput.readthedocs.io/en/latest/index.html
* Solver : https://github.com/dessant/buster

Komut Listesi

None<link>link
    "ilgili linke git."

None<wait_for>title, path, scrolldown_enabled=False, scrollup_enabled=False, try_limit=3
    "İlgili görsel bulunana kadar bekle."
    +title              = "Başlık"
    +path               = "Hangi görselin bulunması beklenecek." (!) Eğer ki path dizinse, dizin altındaki bütün görseller aranır.
    +scrolldown_enabled = "Görsel aranırken scrollbar aşağıya  kaydırılsın mı?"
    +scrollup_enabled   = "Görsel aranırken scrollbar yukarıya kaydırılsın mı?"
    +try_limit          = "Eğer aramada scrolldown_enabled aktifse ve sayfa sonuna kadar içerik bulunamamışsa, sayfa başına gidilir ve counter arttırılır. Counter limit dolduğunda arama sonlandırılır.

find_and_click>path
    "İlgili görselin merkezi tespit edilip, tıklanır."
    +path               = "Bulunacak imgenin dosya konumu."

Extra:
    go_to_top
    go_to_bottom
    '' or ImgePozisyonu <find>path, center=False


#Name:Bitcoinker
link>https://bitcoinker.com/
wait_for>"HTML is done?", r'assets/linkedin/htmlisdone.png', scrolldown_enabled=True
wait_for>"I'am not a robot bulunacak.", , scrolldown_enabled=True
find_and_click>r'assets\bitcoinker\claim_bitcoin.png'
wait_for>asoda
find_and_click>aksd







