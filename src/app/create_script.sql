

CREATE TABLE IF NOT EXISTS validations (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name VARCHAR,
date DATE DEFAULT CURRENT_DATE
);
  
CREATE TABLE IF NOT EXISTS instructions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    'name' VARCHAR,
    file_path VARCHAR,
    validation_date DATE DEFAULT CURRENT_DATE,
    expiration_date DATE
);

INSERT INTO instructions ( name, file_path, expiration_date ) VALUES
('PLNR 02.06 Blokovanie dielov','../../resources/pdf/PLNR 02.06 Blokovanie dielov.pdf','2024-07-25'),
('PLNR 03.03 Proces riesenia poskodenia stillage B-C','../../resources/pdf/PLNR 03.03 Proces riesenia poskodenia stillage B-C.pdf','2024-07-25'),
('PLNR 04.02 Nedostatok zamestnancov na zmene','../../resources/pdf/PLNR 04.02 Nedostatok zamestnancov na zmene.pdf','2024-07-25'),
('PLNR 05.05 Príjem nákladného vozidla vo WHS Nitra','../../resources/pdf/PLNR 05.05 Príjem nákladného vozidla vo WHS Nitra.pdf','2024-07-25'),  
('PLNR 07.02 Manažment zmien','../../resources/pdf/PLNR 07.02 Manažment zmien.pdf','2024-07-25'),
('PLNR 10.02 Quality audits','../../resources/pdf/PLNR 10.02 Quality audits.pdf','2024-07-25'),
('PLNR 11.05 Batch finálna kontrola','../../resources/pdf/PLNR 11.05 Batch finálna kontrola.pdf','2024-07-25'),
('PLNR 13.01 TLS monitoring JIS','../../resources/pdf/PLNR 13.01 TLS monitoring JIS.pdf','2024-07-25'),
('PLNR 14.01 ASN-Advanced shipment notice','../../resources/pdf/PLNR 14.01 ASN-Advanced shipment notice.pdf','2024-07-25'),
('PLNR 15.01 Kontrola vozíkov a zdvíhacieho zariadenia','../../resources/pdf/PLNR 15.01 Kontrola vozíkov a zdvíhacieho zariadenia.pdf','2024-07-25'),
('PLNR ADMIN 01.03 Kontrola prepravnych dokumentov','../../resources/pdf/PLNR ADMIN 01.03 Kontrola prepravnych dokumentov.pdf','2024-07-25'),
('PLNR IAC 01.03 Prijem materialu IAC JIS','../../resources/pdf/PLNR IAC 01.03 Prijem materialu IAC JIS.pdf','2024-07-25'),
('PLNR IAC 02 03 Znovuzasobenie materialu IAC JIS','../../resources/pdf/PLNR IAC 02 03 Znovuzasobenie materialu IAC JIS.pdf','2024-07-25'),
('PLNR IAC 03.06 Vychystávanie materiálu IAC JIS','../../resources/pdf/PLNR IAC 03.06 Vychystávanie materiálu IAC JIS.pdf','2024-07-25'),
('PLNR IAC 04.05 Finalna kontrola materialu IAC JIS','../../resources/pdf/PLNR IAC 04.05 Finalna kontrola materialu IAC JIS.pdf','2024-07-25'),
('PLNR IAC 05.02 Nakladka_expedicia IAC JIS','../../resources/pdf/PLNR IAC 05.02 Nakladka_expedicia IAC JIS.pdf','2024-07-25'),
('PLNR IAC 06.02 Príjem a kontrola prázdnych stillage B-C','../../resources/pdf/PLNR IAC 06.02 Príjem a kontrola prázdnych stillage B-C.pdf','2024-07-25'),
('PLNR IAC 08.01 Cycle counting','../../resources/pdf/PLNR IAC 08.01 Cycle counting.pdf','2024-07-25'),
('PLNR IAC 09.04 Blokovane diely IAC Zona blokovanych dielov IAC','../../resources/pdf/PLNR IAC 09.04 Blokovane diely IAC Zona blokovanych dielov IAC.pdf','2024-07-25'),
('PLNR IAC 12.01 Eskalacny proces','../../resources/pdf/PLNR IAC 12.01 Eskalacny proces.pdf','2024-07-25'),
('PLNR IAC 13.01 Internal Buffer monitor','../../resources/pdf/PLNR IAC 13.01 Internal Buffer monitor.pdf','2024-07-25'),
('PLNR IAC 14.01 Nahradne balenie-nedostatok stillage B-C','../../resources/pdf/PLNR IAC 14.01 Nahradne balenie-nedostatok stillage B-C.pdf','2024-07-25'),
('PLNR IAC 15.01 Krížové zámeny','../../resources/pdf/PLNR IAC 15.01 Krížové zámeny.pdf','2024-07-25'),
('PLNR IAC 16.01 Riadenie NOK KUK dielov _ replacement IAC_ reorder  JLR','../../resources/pdf/PLNR IAC 16.01 Riadenie NOK KUK dielov _ replacement IAC_ reorder  JLR.pdf','2024-07-25'),
('PLNR IAC 17.01 Shortage','../../resources/pdf/PLNR IAC 17.01 Shortage.pdf','2024-07-25'),
('PLNR IFM 01-02 Skener -Prihlásenie Login','../../resources/pdf/PLNR IFM 01-02 Skener -Prihlásenie Login.pdf','2024-07-25'),
('PLNR LEAR 01.06 Prijem materialu LEAR','../../resources/pdf/PLNR LEAR 01.06 Prijem materialu LEAR.pdf','2024-07-25'),
('PLNR LEAR 02.03 Uskladnenie  materiálu','../../resources/pdf/PLNR LEAR 02.03 Uskladnenie  materiálu.pdf','2024-07-25'),
('PLNR LEAR 03.05 KSK Cabin Dekantovanie','../../resources/pdf/PLNR LEAR 03.05 KSK Cabin Dekantovanie.pdf','2024-07-25'),
('PLNR LEAR 04.02 KSK Engine Dekantovanie','../../resources/pdf/PLNR LEAR 04.02 KSK Engine Dekantovanie.pdf','2024-07-25'),
('PLNR LEAR 05.03 JIS znovuzásobenie','../../resources/pdf/PLNR LEAR 05.03 JIS znovuzásobenie.pdf','2024-07-25'),
('PLNR LEAR 08.07 JIS - proces vychystávania KZV','../../resources/pdf/PLNR LEAR 08.07 JIS - proces vychystávania KZV.pdf','2024-07-25'),
('PLNR LEAR 09.05 Vychystávanie materiálu BATCH na expedíciu','../../resources/pdf/PLNR LEAR 09.05 Vychystávanie materiálu BATCH na expedíciu.pdf','2024-07-25'),       
('PLNR LEAR 10.06 Vychystavanie BUSBAR','../../resources/pdf/PLNR LEAR 10.06 Vychystavanie BUSBAR.pdf','2024-07-25'),
('PLNR LEAR 11.08 Finálna kontrola JIS,KSK, Megaharness','../../resources/pdf/PLNR LEAR 11.08 Finálna kontrola JIS,KSK, Megaharness.pdf','2024-07-25'),
('PLNR LEAR 12.02 Príjem a kontrola prázdnych stillage','../../resources/pdf/PLNR LEAR 12.02 Príjem a kontrola prázdnych stillage.pdf','2024-07-25'),
('PLNR LEAR 13.06 Skladovanie, skladanie a expedicia vratných obalov','../../resources/pdf/PLNR LEAR 13.06 Skladovanie, skladanie a expedicia vratných obalov.pdf','2024-07-25'),
('PLNR LEAR 14.01-A Inžinierske zmeny','../../resources/pdf/PLNR LEAR 14.01-A Inžinierske zmeny.pdf','2024-07-25'),
('PLNR LEAR 15.03 Nakládka – Expedícia JIS _ KSK','../../resources/pdf/PLNR LEAR 15.03 Nakládka – Expedícia JIS _ KSK.pdf','2024-07-25'),
('PLNR LEAR 16.05 Nakladka expedicia BATCH  BUSBAR','../../resources/pdf/PLNR LEAR 16.05 Nakladka expedicia BATCH  BUSBAR.pdf','2024-07-25'),
('PLNR LEAR 17.03 Cycle count','../../resources/pdf/PLNR LEAR 17.03 Cycle count.pdf','2024-07-25'),
('PLNR LEAR 18.04 Celková inventúra','../../resources/pdf/PLNR LEAR 18.04 Celková inventúra.pdf','2024-07-25'),
('PLNR LEAR 21.02 CHEP - Kontrola, Evidencia, Skladovanie','../../resources/pdf/PLNR LEAR 21.02 CHEP - Kontrola, Evidencia, Skladovanie.pdf','2024-07-25'),
('PLNR LEAR 22.04 Vytvorenie vlny','../../resources/pdf/PLNR LEAR 22.04 Vytvorenie vlny.pdf','2024-07-25'),
('PLNR LEAR 25.01 Internal Buffer Tracker','../../resources/pdf/PLNR LEAR 25.01 Internal Buffer Tracker.pdf','2024-07-25'),
('PLNR LEAR 26.01 Shortage','../../resources/pdf/PLNR LEAR 26.01 Shortage.pdf','2024-07-25'),
('PLNR LEAR 27.03 KSK Cabin, Engine, Megaharness- Vychystávanie dielov','../../resources/pdf/PLNR LEAR 27.03 KSK Cabin, Engine, Megaharness- Vychystávanie dielov.pdf','2024-07-25'),
('PLNR LEAR 28.01 Kontrola kondície vratných drevených paliet','../../resources/pdf/PLNR LEAR 28.01 Kontrola kondície vratných drevených paliet.pdf','2024-07-25'),     
('PLNR LEAR 29.01 Reprint TLS etikety','../../resources/pdf/PLNR LEAR 29.01 Reprint TLS etikety.pdf','2024-07-25'),
('PLNR MIND 01.02 Príjem a zaskladnenie materiálu','../../resources/pdf/PLNR MIND 01.02 Príjem a zaskladnenie materiálu.pdf','2024-07-25'),
('PLNR MIND 02.02 Vychystávanie - prebal materiálu a príprava na expedíciu','../../resources/pdf/PLNR MIND 02.02 Vychystávanie - prebal materiálu a príprava na expedíciu.pdf','2024-07-25'),
('PLNR MIND 03.02 Nakládka a expedícia','../../resources/pdf/PLNR MIND 03.02 Nakládka a expedícia.pdf','2024-07-25'),
('PNRIAC 11.01 Proces monitorovania skladovych zasob','../../resources/pdf/PNRIAC 11.01 Proces monitorovania skladovych zasob.pdf','2024-07-25');

/*random test values for histogram*/
INSERT INTO validations (name, date)
VALUES 
  ('Alice Johnson', '2023-01-30'),
  ('Alice Johnson', '2022-01-30'),
  ('Alice Johnson', '2023-02-01'),
  ('Alice Johnson', '2023-07-30');

