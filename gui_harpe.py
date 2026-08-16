import customtkinter as ctk
import hid
import time
import threading

VID, PID = 0x0B05, 0x1A94

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('blue')

class HarpeApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('ROG Harpe Ace Control Center')
        self.geometry('600x450')
        self.resizable(False, False)

        self.tabview = ctk.CTkTabview(self, width=560, height=410)
        self.tabview.pack(padx=20, pady=10)

        self.tab_battery = self.tabview.add('Batteria')
        self.tab_dpi = self.tabview.add('DPI & Performance')
        self.tab_profiles = self.tabview.add('Profili & Info')

        self._setup_battery_tab()
        self._setup_dpi_tab()
        self._setup_profiles_tab()

        self.update_battery_thread()

    def _setup_battery_tab(self):
        self.lbl_title = ctk.CTkLabel(self.tab_battery, text='Stato ROG Harpe Ace', font=('Segoe UI', 20, 'bold'))
        self.lbl_title.pack(pady=15)

        self.progress_batt = ctk.CTkProgressBar(self.tab_battery, width=350, height=20)
        self.progress_batt.pack(pady=15)
        self.progress_batt.set(0)

        self.lbl_batt_pct = ctk.CTkLabel(self.tab_battery, text='Lettura in corso...', font=('Segoe UI', 16))
        self.lbl_batt_pct.pack(pady=5)

        self.lbl_status = ctk.CTkLabel(self.tab_battery, text='', font=('Segoe UI', 13), text_color='gray')
        self.lbl_status.pack(pady=5)

        self.btn_refresh = ctk.CTkButton(self.tab_battery, text='Aggiorna Ora', command=self.read_battery)
        self.btn_refresh.pack(pady=20)

    def _setup_dpi_tab(self):
        ctk.CTkLabel(self.tab_dpi, text='Configurazione DPI (In Sviluppo)', font=('Segoe UI', 16, 'bold')).pack(pady=15)
        self.slider_dpi = ctk.CTkSlider(self.tab_dpi, from_=100, to=36000, number_of_steps=359)
        self.slider_dpi.pack(pady=10)
        self.slider_dpi.set(800)
        self.lbl_dpi_val = ctk.CTkLabel(self.tab_dpi, text='DPI Selezionati: 800', font=('Segoe UI', 14))
        self.lbl_dpi_val.pack(pady=5)

        def on_dpi_change(val):
            self.lbl_dpi_val.configure(text=f'DPI Selezionati: {int(val)}')

        self.slider_dpi.configure(command=on_dpi_change)

    def _setup_profiles_tab(self):
        ctk.CTkLabel(self.tab_profiles, text='Profili & Info Dispositivo', font=('Segoe UI', 16, 'bold')).pack(pady=15)
        ctk.CTkLabel(self.tab_profiles, text='VID: 0x0B05 | PID: 0x1A94 - ROG Harpe Ace').pack(pady=10)

    def read_battery(self):
        def _read():
            dev = None
            try:
                target_path = None
                for d in hid.enumerate(VID, PID):
                    if d.get('interface_number') == 0:
                        target_path = d.get('path')
                        break

                if not target_path:
                    self.lbl_batt_pct.configure(text='Mouse non trovato')
                    return

                dev = hid.device()
                dev.open_path(target_path)

                for sub in range(0x00, 0x09):
                    req = [0x00, 0x12, sub, 0x00] + [0x00] * 60
                    dev.write(bytes(req))
                    time.sleep(0.04)
                    res = dev.read(64, timeout_ms=100)
                    if sub == 0x08 and res and res[0] == 0x12:
                        pct = res[4]
                        charging = res[5] == 1
                        self.progress_batt.set(pct / 100.0)
                        self.lbl_batt_pct.configure(text=f'{pct}%')
                        self.lbl_status.configure(text='In Carica (Cavo)' if charging else 'Modalita Wireless')
            except Exception as e:
                print(f'Errore di lettura: {e}')
                self.lbl_batt_pct.configure(text='Errore Connessione')
            finally:
                if dev:
                    dev.close()

        threading.Thread(target=_read, daemon=True).start()

    def update_battery_thread(self):
        self.read_battery()
        self.after(30000, self.update_battery_thread)

if __name__ == '__main__':
    app = HarpeApp()
    app.mainloop()
