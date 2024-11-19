# -*- coding: cp1252 -*-
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from datetime import date

komponenten = {
    'Laptop': [
        {
            'name': 'ThinkBook 16 Gen 6 (Intel) 32GB RAM',
            'preis': 824.47,
            'eigenschaften': {
                'RAM': '32GB',
                'CPU': 'Intel Core i7',
                'GPU': 'Integriert',
                'Besonderheiten': 'Schnellladefunktion – lädt in nur einer Stunde bis zu 80% auf.',
                'Notizen': 'Ideal für Nutzer, die Mobilität schätzen.'
            },
            'bild': 'images/thinkbook.jpg'
        },
        {
            'name': 'HP Pavilion Plus 14-ew1175ng 32GB RAM',
            'preis': 1099.00,
            'eigenschaften': {
                'RAM': '32GB',
                'CPU': 'Intel Core i7',
                'GPU': 'Integriert',
                'Besonderheiten': 'OLED Display mit tiefen Schwarztönen und hervorragender Bildqualität.',
                'Notizen': 'Für Standard-Büroanwendungen ist die günstigere Alternative ausreichend.'
            },
            'bild': 'images/hp_pavilion.jpg'
        }
    ],
    'Docking Station': [
        {
            'name': 'ThinkPad Universal USB-C Dock',
            'preis': 194.66,
            'eigenschaften': {
                'Besonderheiten': 'Unterstützt mehrere 4K-Displays'
            },
            'bild': 'images/thinkpad_dock.jpg'
        },
        {
            'name': 'HP USB-C Dockingstation G5',
            'preis': 135.01,
            'eigenschaften': {
                'Besonderheiten': '100W Power Delivery'
            },
            'bild': 'images/hp_dock.jpg'
        }
    ],
    'Tastatur/Maus': [
        {
            'name': 'Amazon Basics - Kabellos',
            'preis': 24.29,
            'eigenschaften': {
                'Besonderheiten': 'Kabellos'
            },
            'bild': 'images/amazon_keyboard.jpg'
        },
        {
            'name': 'Amazon Basics - Ergonomisch, Kabellos',
            'preis': 30.00,
            'eigenschaften': {
                'Besonderheiten': 'Kabellos, Ergonomisch',
                'Notizen': 'Ideal für Nutzer, die Wert auf Ergonomie legen.'
            },
            'bild': 'images/amazon_ergonomic_keyboard.jpg'
        }
    ],
    'Monitor': [
        {
            'name': 'Dell 27-Monitor – SE2725H',
            'preis': 100.31,
            'eigenschaften': {
                'Größe': '27 Zoll',
                'Auflösung': 'Full HD',
                'Besonderheiten': '75Hz',
                'Notizen': 'Gut für Standard-Büroanwendungen.'
            },
            'bild': 'images/dell_monitor.jpg'
        },
        {
            'name': 'LG Electronics 27UP85NP-W 4K - 27',
            'preis': 270.42,
            'eigenschaften': {
                'Größe': '27 Zoll',
                'Auflösung': '4K UHD',
                'Besonderheiten': 'Hohe Auflösung für detaillierte Grafiken'
            },
            'bild': 'images/lg_monitor.jpg'
        }
    ],
    'Schreibtisch': [
        {
            'name': 'FlexiSpot QS2',
            'preis': 307.01,
            'eigenschaften': {
                'Besonderheiten': 'Höhenverstellbar'
            },
            'bild': 'images/flexispot_desk.jpg'
        },
        {
            'name': 'HomeOne Schreibtisch',
            'preis': 329.99,
            'eigenschaften': {
                'Besonderheiten': 'Höhenverstellbar'
            },
            'bild': 'images/homeone_desk.jpg'
        }
    ],
    'Kopfhörer': [
        {
            'name': 'Go Work Wireless & Wired On-Ear-Headset',
            'preis': 59.99,
            'eigenschaften': {
                'Besonderheiten': 'Rotierende Ohrmuscheln für Brillenträger'
            },
            'bild': 'images/go_work_headset.jpg'
        },
        {
            'name': 'Sony WF-1000XM4',
            'preis': 244.99,
            'eigenschaften': {
                'Besonderheiten': 'Noise-Cancelling'
            },
            'bild': 'images/sony_headphones.jpg'
        }
    ]
}

root = tk.Tk()
root.title("Auswahl der Hardware-Komponenten")
root.geometry('1300x800')

ausgewaehlte_optionen = {}
anzahl_setups_var = tk.IntVar(value=1)

def komponenten_anzeigen(kategorie):
    for widget in inhalt_frame.winfo_children():
        widget.destroy()
    
    optionen = komponenten.get(kategorie, [])
    for idx, item in enumerate(optionen):
        frame = ttk.Frame(inhalt_frame, relief='raised', borderwidth=1)
        frame.grid(row=idx, column=0, padx=10, pady=10, sticky='nsew')
        try:
            img = Image.open(item['bild'])
            img = img.resize((150, 150))
            photo = ImageTk.PhotoImage(img)
            label_bild = ttk.Label(frame, image=photo)
            label_bild.image = photo 
            label_bild.grid(row=0, column=0, rowspan=6, padx=5, pady=5)
        except Exception as e:
            print(f"Fehler beim Laden des Bildes: {e}")
            label_bild = ttk.Label(frame, text='Kein Bild')
            label_bild.grid(row=0, column=0, rowspan=6, padx=5, pady=5)
        
        details = f"Name: {item['name']}\n"
        details += f"Preis: €{item['preis']}\n"
        for eigenschaft, wert in item.get('eigenschaften', {}).items():
            details += f"{eigenschaft}: {wert}\n"
        
        label_details = ttk.Label(frame, text=details)
        label_details.grid(row=0, column=1, padx=10, pady=5, sticky='nw')
        
        anzahl_var = tk.IntVar(value=1)
        def select_item(item=item, anzahl_var=anzahl_var):
            try:
                anzahl = int(anzahl_var.get())
                if anzahl <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Ungültige Anzahl", "Bitte geben Sie eine gültige Anzahl pro Setup ein (positive ganze Zahl).")
                return
            ausgewaehlte_optionen[kategorie] = {'item': item, 'anzahl_pro_setup': anzahl}
            aktualisiere_auswahl_frame()
        
        anzahl_label = ttk.Label(frame, text="Anzahl pro Setup:")
        anzahl_label.grid(row=5, column=1, sticky='w', padx=10)
        anzahl_entry = ttk.Entry(frame, textvariable=anzahl_var, width=5)
        anzahl_entry.grid(row=5, column=1, padx=120, sticky='w')
        
        btn_auswaehlen = ttk.Button(frame, text='Auswählen', command=select_item)
        btn_auswaehlen.grid(row=5, column=1, padx=10, pady=5, sticky='e')
    
    inhalt_frame.update_idletasks()
    canvas_content.configure(scrollregion=canvas_content.bbox("all"))

def aktualisiere_auswahl_frame():
    for widget in auswahl_frame.winfo_children():
        widget.destroy()
    
    tk.Label(auswahl_frame, text="Ausgewählte Komponenten:", font=('Helvetica', 14, 'bold')).pack(pady=5)
    for kategorie, daten in ausgewaehlte_optionen.items():
        item = daten['item']
        anzahl_pro_setup = daten['anzahl_pro_setup']
        tk.Label(auswahl_frame, text=f"{kategorie}: {item['name']} (€{item['preis']}) x {anzahl_pro_setup} pro Setup", wraplength=250).pack(anchor='w')
    
    anzahl_setups_frame = ttk.Frame(auswahl_frame)
    anzahl_setups_frame.pack(pady=10)
    ttk.Label(anzahl_setups_frame, text="Anzahl der Setups:").pack(side='left')
    ttk.Entry(anzahl_setups_frame, textvariable=anzahl_setups_var, width=5).pack(side='left', padx=5)
    
    tk.Button(auswahl_frame, text='Angebot erstellen', command=auswahl_abschliessen).pack(pady=20)
    
    auswahl_frame.update_idletasks()
    canvas_selection.configure(scrollregion=canvas_selection.bbox("all"))

def auswahl_abschliessen():
    if not ausgewaehlte_optionen:
        messagebox.showwarning("Keine Auswahl", "Bitte wählen Sie mindestens eine Komponente aus.")
        return

    try:
        anzahl_setups = int(anzahl_setups_var.get())
        if anzahl_setups <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Ungültige Anzahl", "Bitte geben Sie eine gültige Anzahl der Setups ein (positive ganze Zahl).")
        return

    gesamtpreise = {}
    mengenrabatt = 0
    gesamtmenge_komponenten = {}
    zusammenfassung_positionen = []
    position_counter = 1
    for kategorie, daten in ausgewaehlte_optionen.items():
        item = daten['item']
        anzahl_pro_setup = daten['anzahl_pro_setup']
        gesamtmenge = anzahl_pro_setup * anzahl_setups
        gesamtmenge_komponenten[kategorie] = gesamtmenge
        preis = item['preis'] * gesamtmenge
        gesamtpreise[kategorie] = preis
        zusammenfassung_positionen.append({
            'position': position_counter,
            'anzahl': gesamtmenge,
            'einheit': 'Stück',
            'bezeichnung': item['name'],
            'einzelpreis': item['preis'],
            'gesamtpreis': preis,
            'bild': item['bild']
        })
        position_counter += 1

    basis_gesamtpreis = sum(gesamtpreise.values())

    gewinn = basis_gesamtpreis * 0.15
    handlungskosten = basis_gesamtpreis * 0.15

    zusammenfassung_positionen.append({
        'position': position_counter,
        'anzahl': '',
        'einheit': '-',
        'bezeichnung': 'Gewinn 15%',
        'einzelpreis': '',
        'gesamtpreis': gewinn,
        'bild': None
    })
    position_counter += 1

    zusammenfassung_positionen.append({
        'position': position_counter,
        'anzahl': '',
        'einheit': '-',
        'bezeichnung': 'Gemein- und Handlungskosten 15%',
        'einzelpreis': '',
        'gesamtpreis': handlungskosten,
        'bild': None
    })
    position_counter += 1

    lieferkosten = 30 * anzahl_setups
    zusammenfassung_positionen.append({
        'position': position_counter,
        'anzahl': anzahl_setups,
        'einheit': '-',
        'bezeichnung': 'Lieferkosten €30 pro Setup',
        'einzelpreis': '',
        'gesamtpreis': lieferkosten,
        'bild': None
    })
    position_counter += 1

    installation_stunden = 3 * anzahl_setups
    installation_preis_pro_stunde = 70.00
    installation_gesamtpreis = installation_stunden * installation_preis_pro_stunde
    zusammenfassung_positionen.append({
        'position': position_counter,
        'anzahl': installation_stunden,
        'einheit': 'Stunden',
        'bezeichnung': 'Installation Arbeitsplatz',
        'einzelpreis': installation_preis_pro_stunde,
        'gesamtpreis': installation_gesamtpreis,
        'bild': None
    })
    position_counter += 1

    zwischensumme_vor_rabatten = basis_gesamtpreis + gewinn + handlungskosten + lieferkosten + installation_gesamtpreis

    kundenrabatt = zwischensumme_vor_rabatten * 0.05  

    zusammenfassung_positionen.append({
        'position': position_counter,
        'anzahl': '-5%',
        'einheit': '-',
        'bezeichnung': 'Kundenrabatt',
        'einzelpreis': '',
        'gesamtpreis': -kundenrabatt,
        'bild': None
    })
    position_counter += 1

    for kategorie, gesamtmenge in gesamtmenge_komponenten.items():
        if gesamtmenge >= 10:
            rabatt = gesamtpreise[kategorie] * 0.05
            mengenrabatt += rabatt
            zusammenfassung_positionen.append({
                'position': position_counter,
                'anzahl': '-5%',
                'einheit': '-',
                'bezeichnung': f'Mengenrabatt auf {kategorie}',
                'einzelpreis': '',
                'gesamtpreis': -rabatt,
                'bild': None
            })
            position_counter += 1

    gesamtpreis_vor_ust = zwischensumme_vor_rabatten - kundenrabatt - mengenrabatt

    ust = installation_gesamtpreis * 0.19  

    gesamtpreis = gesamtpreis_vor_ust + ust

    zeige_zusammenfassung(zusammenfassung_positionen, gesamtpreis_vor_ust, ust)

def zeige_zusammenfassung(positionen, gesamtpreis_vor_ust, ust):
    zusammenfassung_fenster = tk.Toplevel(root)
    zusammenfassung_fenster.title("Zusammenfassung")
    zusammenfassung_fenster.geometry('800x600')

    canvas = tk.Canvas(zusammenfassung_fenster)
    scrollbar = ttk.Scrollbar(zusammenfassung_fenster, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    tk.Label(scrollable_frame, text="Zusammenfassung Ihrer Auswahl:", font=('Helvetica', 14, 'bold')).pack(pady=10)

    for pos in positionen:
        frame = ttk.Frame(scrollable_frame, relief='raised', borderwidth=1)
        frame.pack(fill='x', padx=10, pady=5)

        if pos['bild']:
            try:
                img = Image.open(pos['bild'])
                img = img.resize((100, 100))
                photo = ImageTk.PhotoImage(img)
                label_bild = ttk.Label(frame, image=photo)
                label_bild.image = photo 
                label_bild.grid(row=0, column=0, rowspan=4, padx=5, pady=5)
            except Exception as e:
                print(f"Fehler beim Laden des Bildes: {e}")
                label_bild = ttk.Label(frame, text='Kein Bild')
                label_bild.grid(row=0, column=0, rowspan=4, padx=5, pady=5)
        else:
            label_bild = ttk.Label(frame, text='')
            label_bild.grid(row=0, column=0, rowspan=4, padx=5, pady=5)

        details = f"Position {pos['position']}: {pos['bezeichnung']}\n"
        if pos['anzahl'] != '':
            details += f"Anzahl: {pos['anzahl']} {pos['einheit']}\n"
        if pos['einzelpreis'] != '':
            details += f"Einzelpreis: €{pos['einzelpreis']:.2f}\n"
        details += f"Gesamtpreis: €{pos['gesamtpreis']:.2f}\n"

        ttk.Label(frame, text=details).grid(row=0, column=1, sticky='w')

    summen_frame = ttk.Frame(scrollable_frame)
    summen_frame.pack(pady=10)

    ttk.Label(summen_frame, text=f"Gesamtpreis vor USt: €{gesamtpreis_vor_ust:.2f}", font=('Helvetica', 12, 'bold')).pack(anchor='e')
    ttk.Label(summen_frame, text=f"zzgl. 19% USt auf Dienstleistungen: €{ust:.2f}", font=('Helvetica', 12, 'bold')).pack(anchor='e')
    ttk.Label(summen_frame, text=f"Endgültiger Gesamtpreis: €{gesamtpreis_vor_ust + ust:.2f}", font=('Helvetica', 12, 'bold')).pack(anchor='e')

    button_frame = ttk.Frame(scrollable_frame)
    button_frame.pack(pady=10)

    def pdf_erstellen():
        zusammenfassung_fenster.destroy()
        erstelle_pdf(positionen, gesamtpreis_vor_ust, ust)
        messagebox.showinfo("Angebot erstellt", "Das Angebot wurde erfolgreich als 'Angebot.pdf' gespeichert.")

    ttk.Button(button_frame, text='PDF erstellen', command=pdf_erstellen).pack(side='left', padx=10)
    ttk.Button(button_frame, text='Abbrechen', command=zusammenfassung_fenster.destroy).pack(side='left', padx=10)

def erstelle_pdf(positionen, gesamtpreis_vor_ust, ust):
    c = canvas.Canvas("Angebot.pdf", pagesize=A4)
    width, height = A4

    firma_info = [
        "Wicked GmbH",
        "Hauptstraße 3",
        "22459 Hamburg",
        "Tel: +49 (0)40 12345678",
        "E-Mail: vertrieb@wicked.de",
        "Webseite: www.wicked.de"
    ]

    kunde_info = [
        "ScooTeq GmbH",
        "Dratelnstraße 26",
        "21109 Hamburg"
    ]

    y = height - 50
    for zeile in firma_info:
        c.drawString(30, y, zeile)
        y -= 12

    c.drawString(400, height - 50, "Angebot")
    c.drawString(400, height - 65, f"Datum: {date.today().strftime('%d.%m.%Y')}")
    c.drawString(400, height - 80, "Angebotsnummer: 2024-1911")

    y -= 50
    for zeile in kunde_info:
        c.drawString(30, y, zeile)
        y -= 12

    y -= 30
    c.setFont("Helvetica-Bold", 10)
    c.drawString(30, y, "Pos.")
    c.drawString(60, y, "Anzahl")
    c.drawString(100, y, "Einheit")
    c.drawString(150, y, "Bezeichnung")
    c.drawString(400, y, "Einzelpreis")
    c.drawString(480, y, "Gesamtpreis")
    y -= 15
    c.line(30, y, 550, y)
    y -= 15
    c.setFont("Helvetica", 10)

    for pos in positionen:
        c.drawString(30, y, str(pos['position']))
        c.drawString(60, y, str(pos['anzahl']))
        c.drawString(100, y, pos['einheit'])
        c.drawString(150, y, pos['bezeichnung'])
        if pos['einzelpreis'] != '':
            c.drawRightString(460, y, f"€{pos['einzelpreis']:.2f}")
        else:
            c.drawString(400, y, "")
        c.drawRightString(540, y, f"€{pos['gesamtpreis']:.2f}")
        y -= 15
        if y < 100:
            c.showPage()
            y = height - 50

    y -= 20
    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(460, y, "Gesamtpreis vor USt:")
    c.drawRightString(540, y, f"€{gesamtpreis_vor_ust:.2f}")
    y -= 15
    c.drawRightString(460, y, "zzgl. 19% USt auf Dienstleistungen:")
    c.drawRightString(540, y, f"€{ust:.2f}")
    y -= 15
    gesamt_brutto = gesamtpreis_vor_ust + ust
    c.drawRightString(460, y, "Endgültiger Gesamtpreis:")
    c.drawRightString(540, y, f"€{gesamt_brutto:.2f}")

    c.showPage()
    c.save()
def create_scrollable_frame(parent):
    canvas_widget = tk.Canvas(parent)
    scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas_widget.yview)
    scrollable_frame = ttk.Frame(canvas_widget)
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas_widget.configure(
            scrollregion=canvas_widget.bbox("all")
        )
    )
    canvas_widget.create_window((0, 0), window=scrollable_frame, anchor='nw')
    canvas_widget.configure(yscrollcommand=scrollbar.set)
    return canvas_widget, scrollable_frame, scrollbar

kategorien_frame = ttk.Frame(root, width=200)
kategorien_frame.pack(side='left', fill='y')


inhalt_canvas = tk.Canvas(root)
inhalt_canvas.pack(side='left', fill='both', expand=True)
canvas_content, inhalt_frame, scrollbar_content = create_scrollable_frame(inhalt_canvas)
canvas_content.pack(side="left", fill="both", expand=True)
scrollbar_content.pack(side="right", fill="y")

auswahl_canvas = tk.Canvas(root, width=300)
auswahl_canvas.pack(side='right', fill='y')
canvas_selection, auswahl_frame, scrollbar_selection = create_scrollable_frame(auswahl_canvas)
canvas_selection.pack(side="left", fill="both", expand=True)
scrollbar_selection.pack(side="right", fill="y")

aktualisiere_auswahl_frame()

tk.Label(kategorien_frame, text="Kategorien", font=('Helvetica', 14, 'bold')).pack(pady=10)
for kategorie in komponenten.keys():
    btn = ttk.Button(kategorien_frame, text=kategorie, width=20, command=lambda c=kategorie: komponenten_anzeigen(c))
    btn.pack(padx=10, pady=5)

root.mainloop()