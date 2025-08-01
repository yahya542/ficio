import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.linear_model import LinearRegression
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import folium
from folium.plugins import MarkerCluster
import webbrowser
import os
from pymoo.algorithms.moo.nsga3 import NSGA3
from pymoo.optimize import minimize
from pymoo.core.problem import Problem
from pymoo.util.ref_dirs import get_reference_directions
from pymoo.config import Config
Config.warnings['not_compiled'] = False

# Model definitions
class RNNModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers):
        super(RNNModel, self).__init__()
        self.rnn = nn.RNN(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        out, _ = self.rnn(x)
        return self.fc(out[:, -1, :])

class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers):
        super(LSTMModel, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        out, _ = self.lstm(x)
        return self.fc(out[:, -1, :])

class GRUModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers):
        super(GRUModel, self).__init__()
        self.gru = nn.GRU(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        out, _ = self.gru(x)
        return self.fc(out[:, -1, :])

class BiLSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers):
        super(BiLSTMModel, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True, bidirectional=True)
        self.fc = nn.Linear(hidden_size * 2, 1)

    def forward(self, x):
        out, _ = self.lstm(x)
        return self.fc(out[:, -1, :])

# Data loading and preprocessing

df_global = None
canvas_widget = None
table_widget = None


def load_data(filepath):
    df = pd.read_csv(filepath)
    df['bulan_normalized'] = df['Bulan'] / 12.0
    df = df.drop(['Tahun', 'Bulan'], axis=1)
    df = pd.get_dummies(df, columns=['jenis_ikan'])
    return df

def prepare_data(df):
    X = df.drop('stok_ikan', axis=1).values
    y = df['stok_ikan'].values.reshape(-1, 1)
    scaler_X = MinMaxScaler()
    scaler_y = MinMaxScaler()
    X_scaled = scaler_X.fit_transform(X)
    y_scaled = scaler_y.fit_transform(y)
    X_scaled = X_scaled.reshape((X_scaled.shape[0], 1, X_scaled.shape[1]))
    return train_test_split(X_scaled, y_scaled, test_size=0.2, random_state=42), scaler_X, scaler_y, X, y

def train_model(model, X_train, y_train, X_test, y_test, num_epochs=200, lr=0.001):
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    for epoch in range(num_epochs):
        model.train()
        outputs = model(torch.tensor(X_train, dtype=torch.float32))
        loss = criterion(outputs, torch.tensor(y_train, dtype=torch.float32))
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    model.eval()
    predictions = model(torch.tensor(X_test, dtype=torch.float32)).detach().numpy()
    mse = mean_squared_error(y_test, predictions)
    mae = mean_absolute_error(y_test, predictions)
    return predictions, mse, mae

def clear_canvas():
    global canvas_widget, table_widget
    if canvas_widget:
        canvas_widget.get_tk_widget().destroy()
        canvas_widget = None
    if table_widget:
        for child in frame_right.winfo_children():
            if isinstance(child, ttk.Scrollbar):
                child.destroy()
        table_widget.destroy()
        table_widget = None

def plot_predictions(models_results, y_test):
    global canvas_widget
    clear_canvas()
    fig, axs = plt.subplots(2, 2, figsize=(10, 8))
    axs = axs.ravel()
    for i, (name, (pred, mse, mae)) in enumerate(models_results.items()):
        axs[i].plot(y_test, label='Actual', color='black')
        axs[i].plot(pred, label='Predicted', linestyle='--')
        axs[i].legend(fontsize=6)
        axs[i].set_title(f"{name}\nMAE: {mae:.2f}, MSE: {mse:.2f}", fontsize=8)
    plt.tight_layout()
    canvas_widget = FigureCanvasTkAgg(fig, master=frame_right)
    canvas_widget.draw()
    canvas_widget.get_tk_widget().pack(fill="both", expand=True)

def show_correlation(df):
    clear_canvas()
    fig, ax = plt.subplots(figsize=(10, 8))
    corr = df.corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
    ax.set_title("Heatmap Korelasi Antar Variabel")
    plt.tight_layout()
    global canvas_widget
    canvas_widget = FigureCanvasTkAgg(fig, master=frame_right)
    canvas_widget.draw()
    canvas_widget.get_tk_widget().pack(fill="both", expand=True)

def show_data_table(df):
    global table_widget
    clear_canvas()
    table_widget = ttk.Treeview(frame_right)
    table_widget.pack(fill="both", expand=True)
    table_widget["columns"] = list(df.columns)
    table_widget["show"] = "headings"
    for col in df.columns:
        table_widget.heading(col, text=col)
        table_widget.column(col, width=100, anchor="center")
    for _, row in df.iterrows():
        table_widget.insert("", "end", values=list(row))
    vsb = ttk.Scrollbar(frame_right, orient="vertical", command=table_widget.yview)
    hsb = ttk.Scrollbar(frame_right, orient="horizontal", command=table_widget.xview)
    table_widget.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    vsb.pack(side="right", fill="y")
    hsb.pack(side="bottom", fill="x")

# NSGA3 Optimization
class FishOptProblem(Problem):
    def __init__(self, X, y):
        super().__init__(n_var=X.shape[1], n_obj=2, n_constr=0, xl=0, xu=1)
        self.X = X
        self.y = y

    def _evaluate(self, X_opt, out, *args, **kwargs):
        preds = X_opt @ self.X.T
        total_pred = preds.sum(axis=1)
        mse = ((preds - self.y.T)**2).mean(axis=1)
        out["F"] = np.column_stack([-total_pred, mse])  # maximize stok ikan, minimize error

def run_optimization():
    if df_global is None:
        messagebox.showwarning("Data Kosong", "Silakan buka data terlebih dahulu.")
        return
    clear_canvas()
    X = df_global.drop('stok_ikan', axis=1).values
    y = df_global['stok_ikan'].values.reshape(-1, 1)
    ref_dirs = get_reference_directions("energy", n_dim=2, n_points=40)
    problem = FishOptProblem(X, y)
    algo = NSGA3(pop_size=40, ref_dirs=ref_dirs)
    res = minimize(problem, algo, ('n_gen', 100), verbose=False)

    fig, ax = plt.subplots()
    ax.scatter(-res.F[:, 0], res.F[:, 1], c='blue')  # restore positive stok ikan values
    ax.set_xlabel("Total Predicted Stok Ikan")
    ax.set_ylabel("MSE")
    ax.set_title("Hasil Optimasi NSGA-III")
    global canvas_widget, table_widget
    canvas_widget = FigureCanvasTkAgg(fig, master=frame_right)
    canvas_widget.draw()
    canvas_widget.get_tk_widget().pack(fill="both", expand=True)

    table_widget = ttk.Treeview(frame_right)
    table_widget.pack(fill="both", expand=True)
    table_widget["columns"] = [f"X{i+1}" for i in range(res.X.shape[1])] + ["Total Stok", "MSE"]
    table_widget["show"] = "headings"
    for col in table_widget["columns"]:
        table_widget.heading(col, text=col)
        table_widget.column(col, width=80, anchor="center")
    for i in range(res.X.shape[0]):
        row = list(res.X[i]) + [-res.F[i, 0], res.F[i, 1]]
        table_widget.insert("", "end", values=[f"{val:.4f}" for val in row])
    vsb = ttk.Scrollbar(frame_right, orient="vertical", command=table_widget.yview)
    hsb = ttk.Scrollbar(frame_right, orient="horizontal", command=table_widget.xview)
    table_widget.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    vsb.pack(side="right", fill="y")
    hsb.pack(side="bottom", fill="x")

    best_idx = np.argmax(-res.F[:, 0] / (res.F[:, 1] + 1e-6))
    best_total, best_mse = -res.F[best_idx, 0], res.F[best_idx, 1]
    messagebox.showinfo("Solusi Terbaik NSGA-III", f"Solusi terbaik:Total Stok Ikan = {best_total:.4f}, MSE = {best_mse:.4f}")

# GUI
results_global = {}
actual_global = None

def open_file():
    global df_global
    file_path = filedialog.askopenfilename()
    if file_path:
        df_global = load_data(file_path)
        messagebox.showinfo("Berhasil", "Data berhasil dimuat.")
        show_data_table(df_global)

def run_prediction():
    global results_global, actual_global
    if df_global is None:
        messagebox.showwarning("Data Kosong", "Silakan buka data terlebih dahulu.")
        return
    (X_train, X_test, y_train, y_test), scaler_X, scaler_y, X_raw, y_raw = prepare_data(df_global)
    input_size = X_train.shape[2]
    hidden_size = 32
    num_layers = 1
    models = {
        'GRU': GRUModel(input_size, hidden_size, num_layers),
        'LSTM': LSTMModel(input_size, hidden_size, num_layers),
        'BiLSTM': BiLSTMModel(input_size, hidden_size, num_layers),
    }
    results = {}
    for name, model in models.items():
        pred, mse, mae = train_model(model, X_train, y_train, X_test, y_test)
        pred = scaler_y.inverse_transform(pred)
        actual = scaler_y.inverse_transform(y_test)
        results[name] = (pred, mse, mae)
    X_train_lr, X_test_lr, y_train_lr, y_test_lr = train_test_split(X_raw, y_raw, test_size=0.2, random_state=42)
    lr_model = LinearRegression()
    lr_model.fit(X_train_lr, y_train_lr)
    y_pred_lr = lr_model.predict(X_test_lr)
    mse_lr = mean_squared_error(y_test_lr, y_pred_lr)
    mae_lr = mean_absolute_error(y_test_lr, y_pred_lr)
    results['Linear Regression'] = (y_pred_lr.reshape(-1, 1), mse_lr, mae_lr)
    results_global = results
    actual_global = actual
    plot_predictions(results, actual)

def export_csv():
    if results_global and actual_global is not None:
        output_df = pd.DataFrame({"Actual": actual_global.flatten()})
        for name, (pred, _, _) in results_global.items():
            output_df[name] = pred.flatten()
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[["CSV files", "*.csv"]])
        if file_path:
            output_df.to_csv(file_path, index=False)
            messagebox.showinfo("Berhasil", "Hasil prediksi berhasil disimpan.")
    else:
        messagebox.showwarning("Data Kosong", "Lakukan prediksi terlebih dahulu.")

def show_correlation_window():
    if df_global is not None:
        show_correlation(df_global)
    else:
        messagebox.showwarning("Data Kosong", "Silakan buka data terlebih dahulu.")

# Main app
root = tk.Tk()
root.title("FishCastAI - Prediksi Perikanan dengan GRU, LSTM, BiLSTM, Regresi Linier, dan NSGA-III")
root.geometry("1100x700")

frame_left = tk.Frame(root)
frame_left.pack(side="left", fill="y", padx=10, pady=10)

frame_right = tk.Frame(root)
frame_right.pack(side="right", fill="both", expand=True, padx=10, pady=10)

btn_open = tk.Button(frame_left, text="Buka Data", command=open_file)
btn_open.pack(pady=5, fill="x")

btn_predict = tk.Button(frame_left, text="Prediksi", command=run_prediction)
btn_predict.pack(pady=5, fill="x")

btn_optim = tk.Button(frame_left, text="Optimasi (NSGA-III)", command=run_optimization)
btn_optim.pack(pady=5, fill="x")

btn_corr = tk.Button(frame_left, text="Korelasi Fitur", command=show_correlation_window)
btn_corr.pack(pady=5, fill="x")

btn_export = tk.Button(frame_left, text="Export CSV", command=export_csv)
btn_export.pack(pady=5, fill="x")

btn_exit = tk.Button(frame_left, text="Keluar", command=root.quit)
btn_exit.pack(pady=5, fill="x")

root.mainloop()
