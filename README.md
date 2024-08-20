# RealEstateSlovenia-Insight
Ta projekt si prizadeva zagotoviti poglobljeno analizo slovenskega nepremičninskega trga, s poudarkom na prodaji in dolgoročnem najemu. Podatki za to analizo so bili pridobljeni s spletnega mesta https://www.nepremicnine.net/, ki zajema širok spekter nepremičninskih oglasov.

Z uporabo knjižnice Pandas v programskem jeziku Python znotraj okolja Jupyter Notebook bo projekt raziskal ključne tržne trende, cenovne vzorce in geografsko razporeditev nepremičnin. S pomočjo vizualizacije teh podatkov in izvedbe statističnih analiz bo projekt poskušal ponuditi dragocene vpoglede v dinamiko slovenskega nepremičninskega trga, kar bi lahko pomagalo kupcem, najemnikom in vlagateljem pri sprejemanju premišljenih odločitev.

# Navodila za uporabo [Linux]

1. Preverite, ali imate nameščen Python: `python3 --version`
2. Preverite, ali imate nameščen Git: `git --version`
3. Klonirajte repozitorij na svoj računalnik: `git clone https://github.com/iruspro/RealEstateSlovenia-Insight`
4. Pojdite v mapo s projektom: `cd RealEstateSlovenia-Insight`
5. Ustvarite novo virtualno okolje: `python3 -m venv env`
6. Aktivirajte virtualno okolje: `source env/bin/activate`
6. Namestite potrebne pakete za delovanje programa: `pip install requests pandas seaborn numpy matplotlib notebook`
7. Zaženite program: `python3 main.py`
8. Zaženite Jupyter Notebook: `jupyter notebook`
9. V odprtem oknu brskalnika izberite datoteko `analysis.ipynb`
10. Kliknite v zgornjem meniju na `Run -> Run All Cells`
11. Uživajte v analizi.

Če želite znova prenesti podatke s spletne strani, izbrišite vsebino mape pages: `rm -rf pages/*` in zaženite program: `python3 main.py`
