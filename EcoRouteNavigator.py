# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
from datetime import datetime
import requests
import folium
import os
import webbrowser

class EScooterApp:
    def __init__(self):
        self.window = tk.Tk()
        self.style = ttk.Style(self.window)
        self.window.title("E-Scooter Assistant")
        self.window.geometry("600x700")
        self.style.theme_use('vista')


        self.basis_preis = 1.00
        self.preis_pro_minute = 0.20
        self.preis_pro_km = 0.30
        
        self.users = self.load_users()
        self.current_user = None
        
        self.create_login_section()
        self.create_main_content()
        
    def load_users(self):
        try:
            with open('users.json', 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
            
    def save_users(self):
        with open('users.json', 'w', encoding='utf-8') as file:
            json.dump(self.users, file, ensure_ascii=False, indent=4)
    
    def create_login_section(self):
        self.login_frame = tk.Frame(self.window)
        self.login_frame.pack(pady=20)
        
        tk.Label(self.login_frame, text="E-Scooter Assistant", 
                font=('Arial', 20, 'bold')).pack(pady=10)
        
        form_frame = tk.Frame(self.login_frame)
        form_frame.pack(pady=10)
        
        tk.Label(form_frame, text="Benutzername:", font=('Arial', 12)).grid(row=0, column=0, sticky='e', pady=5)
        self.username_entry = tk.Entry(form_frame, font=('Arial', 12))
        self.username_entry.grid(row=0, column=1, pady=5)
        
        tk.Label(form_frame, text="Passwort:", font=('Arial', 12)).grid(row=1, column=0, sticky='e', pady=5)
        self.password_entry = tk.Entry(form_frame, show="*", font=('Arial', 12))
        self.password_entry.grid(row=1, column=1, pady=5)
        
        button_frame = tk.Frame(self.login_frame)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Login", 
                 command=self.login, width=12, font=('Arial', 12)).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Registrieren", 
                 command=self.register, width=12, font=('Arial', 12)).pack(side=tk.LEFT, padx=5)

    def create_main_content(self):
        self.main_frame = tk.Frame(self.window)
        
        self.tab_control = ttk.Notebook(self.main_frame)
        
        self.price_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.price_tab, text='Preisrechner')
        self.setup_price_calculator()
        
        self.route_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.route_tab, text='EcoRoute Navigator')
        self.setup_route_planner()
        
        self.tab_control.pack(expand=1, fill='both')
    
    def setup_price_calculator(self):
        calc_frame = tk.Frame(self.price_tab, padx=20, pady=20)
        calc_frame.pack(pady=10)
        
        tk.Label(calc_frame, text="Preisberechnung", 
                font=('Arial', 16, 'bold')).pack(pady=10)
        
        self.calc_method = tk.StringVar(value="time")
        method_frame = tk.Frame(calc_frame)
        method_frame.pack(pady=5)
        tk.Radiobutton(method_frame, text="Nach Zeit", variable=self.calc_method, 
                      value="time", command=self.toggle_input, font=('Arial', 12)).pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(method_frame, text="Nach Strecke", variable=self.calc_method, 
                      value="distance", command=self.toggle_input, font=('Arial', 12)).pack(side=tk.LEFT, padx=10)
        
        self.time_frame = tk.Frame(calc_frame)
        tk.Label(self.time_frame, text="Minuten:", font=('Arial', 12)).pack(side=tk.LEFT)
        self.time_entry = tk.Entry(self.time_frame, width=10, font=('Arial', 12))
        self.time_entry.pack(side=tk.LEFT, padx=5)
        self.time_frame.pack(pady=5)
        
        self.distance_frame = tk.Frame(calc_frame)
        tk.Label(self.distance_frame, text="Kilometer:", font=('Arial', 12)).pack(side=tk.LEFT)
        self.distance_entry = tk.Entry(self.distance_frame, width=10, font=('Arial', 12))
        self.distance_entry.pack(side=tk.LEFT, padx=5)
        self.distance_frame.pack_forget()
        
        tk.Button(calc_frame, text="Preis berechnen", 
                 command=self.calculate_price, font=('Arial', 12), width=15).pack(pady=10)
        
        self.result_label = tk.Label(calc_frame, text="", font=('Arial', 14, 'bold'))
        self.result_label.pack(pady=10)
        
        history_frame = tk.Frame(calc_frame)
        history_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        tk.Label(history_frame, text="Fahrtverlauf", 
                font=('Arial', 14, 'bold')).pack(pady=5)
        self.history_text = tk.Text(history_frame, height=8, width=50, font=('Arial', 12))
        self.history_text.pack(pady=5)
        self.history_text.configure(state='disabled')
        
    def setup_route_planner(self):
        route_frame = tk.Frame(self.route_tab, padx=20, pady=20)
        route_frame.pack(pady=10, fill='both', expand=True)
        
        tk.Label(route_frame, text="EcoRoute Navigator", 
                font=('Arial', 16, 'bold')).pack(pady=10)
        tk.Label(route_frame, text="Finden Sie die beste Route fuer Ihren E-Scooter",
                font=('Arial', 12)).pack(pady=5)
        
        input_frame = tk.Frame(route_frame)
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="Startadresse:", font=('Arial', 12)).grid(row=0, column=0, sticky='e', pady=5)
        self.start_entry = tk.Entry(input_frame, width=30, font=('Arial', 12))
        self.start_entry.grid(row=0, column=1, pady=5, padx=5)
        self.start_entry.bind('<KeyRelease>', self.update_start_autocomplete)
        
        tk.Label(input_frame, text="Zieladresse:", font=('Arial', 12)).grid(row=1, column=0, sticky='e', pady=5)
        self.destination_entry = tk.Entry(input_frame, width=30, font=('Arial', 12))
        self.destination_entry.grid(row=1, column=1, pady=5, padx=5)
        self.destination_entry.bind('<KeyRelease>', self.update_destination_autocomplete)
        
        self.start_listbox = tk.Listbox(input_frame, width=45, font=('Arial', 10))
        self.start_listbox.grid(row=2, column=0, columnspan=2, padx=5)
        self.start_listbox.bind('<<ListboxSelect>>', self.select_start_address)
        self.start_listbox_hide()
        
        self.destination_listbox = tk.Listbox(input_frame, width=45, font=('Arial', 10))
        self.destination_listbox.grid(row=3, column=0, columnspan=2, padx=5)
        self.destination_listbox.bind('<<ListboxSelect>>', self.select_destination_address)
        self.destination_listbox_hide()
        
        tk.Button(route_frame, text="Route berechnen", 
                 command=self.calculate_route, font=('Arial', 12), width=15).pack(pady=10)
        
        self.route_result = tk.Text(route_frame, height=6, width=50, font=('Arial', 12))
        self.route_result.pack(pady=10)
        self.route_result.configure(state='disabled')

    def update_start_autocomplete(self, event):
        query = self.start_entry.get()
        if query:
            suggestions = self.autocomplete_address(query)
            if suggestions:
                self.start_listbox_show(suggestions)
            else:
                self.start_listbox_hide()
        else:
            self.start_listbox_hide()
    
    def start_listbox_show(self, suggestions):
        self.start_listbox.delete(0, tk.END)
        for suggestion in suggestions:
            self.start_listbox.insert(tk.END, suggestion)
        self.start_listbox.lift()
        self.start_listbox.update()
        self.start_listbox.grid()
    
    def start_listbox_hide(self):
        self.start_listbox.grid_remove()
    
    def select_start_address(self, event):
        if self.start_listbox.curselection():
            index = self.start_listbox.curselection()[0]
            selected_address = self.start_listbox.get(index)
            self.start_entry.delete(0, tk.END)
            self.start_entry.insert(0, selected_address)
            self.start_listbox_hide()
    
    def update_destination_autocomplete(self, event):
        query = self.destination_entry.get()
        if query:
            suggestions = self.autocomplete_address(query)
            if suggestions:
                self.destination_listbox_show(suggestions)
            else:
                self.destination_listbox_hide()
        else:
            self.destination_listbox_hide()
    
    def destination_listbox_show(self, suggestions):
        self.destination_listbox.delete(0, tk.END)
        for suggestion in suggestions:
            self.destination_listbox.insert(tk.END, suggestion)
        self.destination_listbox.lift()
        self.destination_listbox.update()
        self.destination_listbox.grid()
    
    def destination_listbox_hide(self):
        self.destination_listbox.grid_remove()
    
    def select_destination_address(self, event):
        if self.destination_listbox.curselection():
            index = self.destination_listbox.curselection()[0]
            selected_address = self.destination_listbox.get(index)
            self.destination_entry.delete(0, tk.END)
            self.destination_entry.insert(0, selected_address)
            self.destination_listbox_hide()
    
    def autocomplete_address(self, query):
        url = 'https://nominatim.openstreetmap.org/search'
        params = {
            'q': query,
            'format': 'json',
            'addressdetails': 1,
            'limit': 5,
        }
        headers = {'User-Agent': 'E-Scooter-App'}
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        suggestions = []
        for item in data:
            display_name = item['display_name']
            suggestions.append(display_name)
        return suggestions
    
    def geocode_address(self, address):
        url = 'https://nominatim.openstreetmap.org/search'
        params = {
            'q': address,
            'format': 'json',
            'limit': 1,
        }
        headers = {'User-Agent': 'E-Scooter-App'}
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        if data:
            lat = float(data[0]['lat'])
            lon = float(data[0]['lon'])
            return [lat, lon]
        else:
            raise Exception("Adresse nicht gefunden.")
    
    def calculate_route(self):

        start_address = self.start_entry.get()
        destination_address = self.destination_entry.get()
        
        try:
            start_coords = self.geocode_address(start_address)
            end_coords = self.geocode_address(destination_address)
            
            url = f"http://router.project-osrm.org/route/v1/bike/{start_coords[1]},{start_coords[0]};{end_coords[1]},{end_coords[0]}?overview=full&geometries=geojson"
            response = requests.get(url)
            data = response.json()
            
            if 'routes' not in data or not data['routes']:
                raise Exception("Keine Route gefunden.")
            
            route_coords = data['routes'][0]['geometry']['coordinates']
            distance = data['routes'][0]['distance'] / 1000  
            duration = data['routes'][0]['duration'] / 60 
            
            m = folium.Map(location=start_coords, zoom_start=14)
            folium.PolyLine(locations=[(lat, lon) for lon, lat in route_coords], color='blue', weight=5).add_to(m)
            
            folium.Marker(location=start_coords, tooltip='Start').add_to(m)
            folium.Marker(location=end_coords, tooltip='Ziel').add_to(m)
            
            map_file = "route_map.html"
            m.save(map_file)
            
            webbrowser.open(f"file://{os.path.abspath(map_file)}")
            
            total_price = self.basis_preis + distance * self.preis_pro_km
            result = f"Distanz: {distance:.2f} km\nGeschaetzte Zeit: {duration:.2f} Minuten\nGeschaetzter Preis: {total_price:.2f}  Euro"
            
            self.route_result.configure(state='normal')
            self.route_result.delete(1.0, tk.END)
            self.route_result.insert(tk.END, result)
            self.route_result.configure(state='disabled')
            
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler bei der Routenberechnung: {e}")

    def toggle_input(self):
        if self.calc_method.get() == "time":
            self.time_frame.pack(pady=5)
            self.distance_frame.pack_forget()
        else:
            self.time_frame.pack_forget()
            self.distance_frame.pack(pady=5)
            
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username in self.users and self.users[username]["password"] == password:
            self.current_user = username
            messagebox.showinfo("Erfolg", f"Willkommen zurueck, {username}!")
            self.login_frame.pack_forget()
            self.main_frame.pack(expand=True, fill='both')
            self.load_history()
        else:
            messagebox.showerror("Fehler", "Ungueltiger Benutzername oder Passwort")
            
    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username and password:
            if username not in self.users:
                self.users[username] = {
                    "password": password,
                    "history": []
                }
                self.save_users()
                messagebox.showinfo("Erfolg", "Registrierung erfolgreich!")
            else:
                messagebox.showerror("Fehler", "Benutzername bereits vergeben")
        else:
            messagebox.showerror("Fehler", "Bitte alle Felder ausfuellen")
            
    def calculate_price(self):
        if not self.current_user:
            messagebox.showerror("Fehler", "Bitte zuerst einloggen")
            return
            
        try:
            total_price = self.basis_preis  
            
            if self.calc_method.get() == "time":
                minutes = float(self.time_entry.get())
                total_price += minutes * self.preis_pro_minute
                usage = f"{minutes} Minuten"
            else:
                kilometers = float(self.distance_entry.get())
                total_price += kilometers * self.preis_pro_km
                usage = f"{kilometers} km"
                
            result_text = f"Gesamtpreis: {total_price:.2f}  Euro"
            self.result_label.config(text=result_text)
            
            self.add_to_history(usage, total_price)
            
        except ValueError:
            messagebox.showerror("Fehler", "Bitte gueltige Zahlen eingeben")
            
    def add_to_history(self, usage, price):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        history_entry = f"{timestamp}: {usage} - {price:.2f}  Euro"
        
        self.users[self.current_user]["history"].append(history_entry)
        self.save_users()
        self.load_history()
        
    def load_history(self):
        self.history_text.configure(state='normal')
        self.history_text.delete(1.0, tk.END)
        if self.current_user:
            history = self.users[self.current_user]["history"]
            for entry in history:
                self.history_text.insert(tk.END, entry + "\n")
        self.history_text.configure(state='disabled')
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = EScooterApp()
    app.run()
