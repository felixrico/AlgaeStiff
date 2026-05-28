import tkinter as tk
from tkinter import filedialog, ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import re
import numpy as np

class DataPlotterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Plotter")

        # Variables
        self.file1_path = None
        self.file2_path = None
        self.merged_df = None
        self.display_df = None
        self.log_x = tk.BooleanVar()
        self.log_y = tk.BooleanVar()
        self.bin_size_x = tk.IntVar(value=10)
        self.bin_size_y = tk.IntVar(value=10)
        self.threshold_val = tk.DoubleVar(value=0.0)
        
        # Axis range variables
        self.x_min = tk.DoubleVar(value=0.0)
        self.x_max = tk.DoubleVar(value=1.0)
        self.y_min = tk.DoubleVar(value=0.0)
        self.y_max = tk.DoubleVar(value=1.0)
        self.use_custom_x_range = tk.BooleanVar(value=False)
        self.use_custom_y_range = tk.BooleanVar(value=False)

        # GUI Elements
        self.setup_gui()

    def setup_gui(self):
        # File Selection
        tk.Button(self.root, text="Select Viscoelastic File", command=self.load_file1).pack()
        tk.Button(self.root, text="Select adhesion File", command=self.load_file2).pack()

        # Merge Button
        tk.Button(self.root, text="Merge Files", command=self.merge_files).pack()

        # Column Selection
        self.x_col = ttk.Combobox(self.root, state="readonly")
        self.x_col.pack()
        self.y_col = ttk.Combobox(self.root, state="readonly")
        self.y_col.pack()

        # Plot Button
        tk.Button(self.root, text="Plot X vs Y", command=self.plot_xy).pack()

        # Histogram Button
        tk.Button(self.root, text="Plot Histograms", command=self.plot_histograms).pack()

        # Log Scale Checkboxes
        tk.Checkbutton(self.root, text="Log X", variable=self.log_x).pack()
        tk.Checkbutton(self.root, text="Log Y", variable=self.log_y).pack()

        # Bin Size Entries for histograms (separate for X and Y)
        tk.Frame(self.root).pack()
        tk.Label(self.root, text="Bin Size X:").pack()
        tk.Entry(self.root, textvariable=self.bin_size_x).pack()
        tk.Label(self.root, text="Bin Size Y:").pack()
        tk.Entry(self.root, textvariable=self.bin_size_y).pack()

        # Threshold controls for hertz_z_c
        tk.Label(self.root, text="Threshold of height (hertz_z_c >):").pack()
        tk.Entry(self.root, textvariable=self.threshold_val).pack()
        tk.Button(self.root, text="Apply Threshold", command=self.apply_threshold).pack()
        tk.Button(self.root, text="Reset Threshold", command=self.reset_threshold).pack()

        # Export buttons
        tk.Button(self.root, text="Export Filtered CSV", command=self.export_filtered).pack()
        tk.Button(self.root, text="Export Summary Stats", command=self.export_summary).pack()
        tk.Button(self.root, text="Export Plot/Histogram", command=self.export_plot).pack()

        # Axis Range Controls
        tk.Label(self.root, text="--- Axis Range Controls ---").pack()
        tk.Checkbutton(self.root, text="Custom X Range", variable=self.use_custom_x_range).pack()
        tk.Label(self.root, text="X Min:").pack()
        tk.Entry(self.root, textvariable=self.x_min).pack()
        tk.Label(self.root, text="X Max:").pack()
        tk.Entry(self.root, textvariable=self.x_max).pack()
        
        tk.Checkbutton(self.root, text="Custom Y Range", variable=self.use_custom_y_range).pack()
        tk.Label(self.root, text="Y Min:").pack()
        tk.Entry(self.root, textvariable=self.y_min).pack()
        tk.Label(self.root, text="Y Max:").pack()
        tk.Entry(self.root, textvariable=self.y_max).pack()

        # Pixel Map Image Button
        tk.Button(self.root, text="Generate Pixel Map Image", command=self.generate_pixel_map).pack()

        # Matplotlib Figure
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack()

    def _clean_col(self, col_name):
        # Normalize column names: remove quotes, replace non-word chars with
        # single underscore, and strip leading/trailing underscores.
        s = str(col_name)
        s = re.sub(r"[\'\"]", "", s)
        s = re.sub(r"\W+", "_", s)
        s = s.strip("_")
        return s
    def load_file1(self):
        self.file1_path = filedialog.askopenfilename()
        if self.file1_path:
            self.file1 = pd.read_csv(self.file1_path, sep=';', header=0)
            self.file1.columns = self.file1.columns.map(self._clean_col)

    def load_file2(self):
        self.file2_path = filedialog.askopenfilename()
        if self.file2_path:
            self.file2 = pd.read_table(self.file2_path, sep='\t')
            self.file2.columns = self.file2.columns.map(self._clean_col)

    def merge_files(self):
        if self.file1_path and self.file2_path:
            self.merged_df = pd.merge(
                self.file1, self.file2,
                left_on='curve_idx', right_on='Position_Index',
                how='outer'
            )
            self.merged_df.columns = self.merged_df.columns.map(self._clean_col)
            # set display_df to full merged copy initially
            self.display_df = self.merged_df.copy()
            self.update_column_options()

    def update_column_options(self):
        df = self.display_df if self.display_df is not None else self.merged_df
        if df is None:
            return
        numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns
        numerical_list = [str(c) for c in numerical_cols.tolist()]
        print("Merged df columns:", df.columns.tolist())
        print("Numerical cols:", numerical_list)
        self.x_col['values'] = numerical_list
        self.y_col['values'] = numerical_list

    def plot_xy(self):
        df = self.display_df if self.display_df is not None else self.merged_df
        if df is not None:
            x_col = self.x_col.get()
            y_col = self.y_col.get()
            print("x_col:", repr(x_col))
            print("y_col:", repr(y_col))
            if x_col and y_col:
                # Replace figure with a single axes for scatter
                self.fig.clf()
                self.ax = self.fig.add_subplot(1, 1, 1)
                self.ax.scatter(df[x_col], df[y_col])
                if self.log_x.get():
                    self.ax.set_xscale('log', base=10)
                if self.log_y.get():
                    self.ax.set_yscale('log', base=10)
                
                # Apply custom axis ranges if enabled
                if self.use_custom_x_range.get():
                    self.ax.set_xlim(self.x_min.get(), self.x_max.get())
                if self.use_custom_y_range.get():
                    self.ax.set_ylim(self.y_min.get(), self.y_max.get())
                
                self.ax.set_xlabel(x_col)
                self.ax.set_ylabel(y_col)
                self.canvas.draw()

    def plot_histograms(self):
        df = self.display_df if self.display_df is not None else self.merged_df
        if df is not None:
            x_col = self.x_col.get()
            y_col = self.y_col.get()
            if x_col and y_col:
                # Replace figure with two side-by-side histogram axes
                self.fig.clf()
                ax1 = self.fig.add_subplot(1, 2, 1)
                ax2 = self.fig.add_subplot(1, 2, 2)
                
                # Create bins for x histogram
                x_data = df[x_col].dropna()
                if self.log_x.get():
                    # For log scale, use only positive values and create logspace bins
                    x_data = x_data[x_data > 0]
                    if len(x_data) > 0:
                        x_min, x_max = x_data.min(), x_data.max()
                        bins_x = np.logspace(np.log10(x_min), np.log10(x_max), self.bin_size_x.get())
                    else:
                        bins_x = self.bin_size_x.get()
                else:
                    bins_x = self.bin_size_x.get()
                
                # Create bins for y histogram
                y_data = df[y_col].dropna()
                if self.log_y.get():
                    # For log scale, use only positive values and create logspace bins
                    y_data = y_data[y_data > 0]
                    if len(y_data) > 0:
                        y_min, y_max = y_data.min(), y_data.max()
                        bins_y = np.logspace(np.log10(y_min), np.log10(y_max), self.bin_size_y.get())
                    else:
                        bins_y = self.bin_size_y.get()
                else:
                    bins_y = self.bin_size_y.get()
                
                ax1.hist(x_data, bins=bins_x, alpha=0.8)
                ax1.set_title(f"Histogram: {x_col}")
                ax1.set_xlabel(x_col)
                ax1.set_ylabel('Count')
                ax2.hist(y_data, bins=bins_y, alpha=0.8)
                ax2.set_title(f"Histogram: {y_col}")
                ax2.set_xlabel(y_col)
                ax2.set_ylabel('Count')

                if self.log_x.get():
                    ax1.set_xscale('log', base=10)
                    ax2.set_xscale('log', base=10)
                if self.log_y.get():
                    ax1.set_yscale('log', base=10)
                    ax2.set_yscale('log', base=10)

                # Apply custom axis ranges if enabled
                if self.use_custom_x_range.get():
                    ax1.set_xlim(self.x_min.get(), self.x_max.get())
                if self.use_custom_y_range.get():
                    ax2.set_xlim(self.y_min.get(), self.y_max.get())

                # Keep the main axis reference pointing to the first subplot
                self.ax = ax1
                self.canvas.draw()

    def apply_threshold(self):
        # Filter display_df to rows where cleaned 'hertz_z_c' > threshold
        if self.merged_df is None:
            print("No data to filter. Merge files first.")
            return
        col = self._clean_col('hertz_z_c')
        if col not in self.merged_df.columns:
            print(f"Column '{col}' not found in data.")
            return
        thr = self.threshold_val.get()
        # Create filtered copy
        filtered = self.merged_df[self.merged_df[col].astype(float).fillna(-float('inf')) > thr]
        self.display_df = filtered
        print(f"Applied threshold {thr} on '{col}': {len(filtered)} rows kept")
        self.update_column_options()

    def reset_threshold(self):
        if self.merged_df is None:
            return
        self.display_df = self.merged_df.copy()
        print("Reset threshold filter; using full merged data")
        self.update_column_options()

    def export_filtered(self):
        if self.display_df is None:
            print("No data to export. Merge files first.")
            return
        path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV files', '*.csv')])
        if not path:
            return
        try:
            # Export only numeric and non-numeric columns as-is
            self.display_df.to_csv(path, index=False)
            print(f"Filtered data exported to {path}")
        except Exception as e:
            print(f"Failed to export filtered data: {e}")

    def export_summary(self):
        if self.display_df is None:
            print("No data to summarize. Merge files first.")
            return
        df = self.display_df
        num = df.select_dtypes(include=['float64', 'int64'])
        if num.shape[1] == 0:
            print("No numeric columns to summarize.")
            return
        try:
            mean = num.mean()
            std = num.std()
            median = num.median()
            q75 = num.quantile(0.75)
            q25 = num.quantile(0.25)
            iqr = q75 - q25

            # Geometric mean: only for positive values
            geom = {}
            for col in num.columns:
                series = num[col].dropna()
                series_pos = series[series > 0]
                if len(series_pos) > 0:
                    gm = float(np.exp(np.log(series_pos).mean()))
                else:
                    gm = float('nan')
                geom[col] = gm
            geom_series = pd.Series(geom)

            stats_df = pd.DataFrame({
                'mean': mean,
                'std': std,
                'median': median,
                'geom_mean': geom_series,
                'IQR': iqr
            })
            # transpose so rows are stats
            stats_df = stats_df.T

            path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV files', '*.csv')])
            if not path:
                return
            stats_df.to_csv(path)
            print(f"Summary statistics exported to {path}")
        except Exception as e:
            print(f"Failed to compute/export summary: {e}")

    def export_plot(self):
        """Export the current plot/histogram as an image file."""
        path = filedialog.asksaveasfilename(
            defaultextension='.png',
            filetypes=[('PNG files', '*.png'), ('PDF files', '*.pdf'), ('JPEG files', '*.jpg')]
        )
        if not path:
            return
        try:
            self.fig.savefig(path, dpi=300, bbox_inches='tight')
            print(f"Plot exported to {path}")
        except Exception as e:
            print(f"Failed to export plot: {e}")

    def generate_pixel_map(self):
        """Generate a 2D image from the selected column based on pixel positions from either file1 or file2."""
        if self.file1 is None or self.file2 is None:
            print("Both viscoelastic and adhesion files must be loaded.")
            return

        col_name = self.x_col.get()
        if not col_name:
            print("No column selected. Please select a column.")
            return

        # Get map size from file1 (viscoelastic)
        map_size_col = 'map_size_x_y_pixels'
        if map_size_col not in self.file1.columns:
            print(f"Column '{map_size_col}' not found in viscoelastic file.")
            return

        try:
            # Parse the first map_size_x_y_pixels value to get dimensions
            map_size_str = str(self.file1[map_size_col].iloc[0])
            import re
            numbers = re.findall(r'\d+', map_size_str)
            if len(numbers) < 2:
                print(f"Could not parse map dimensions from '{map_size_str}'")
                return
            size_x = int(numbers[0])
            size_y = int(numbers[1])
            print(f"Map dimensions: {size_x} x {size_y}")

            # Determine which file contains the column
            if col_name in self.file1.columns:
                data_df = self.file1.sort_values('curve_idx').reset_index(drop=True)
                idx_col = 'curve_idx'
            elif col_name in self.file2.columns:
                data_df = self.file2.sort_values('Position_Index').reset_index(drop=True)
                idx_col = 'Position_Index'
            else:
                print(f"Column '{col_name}' not found in viscoelastic or adhesion file.")
                print(f"Available columns in file1: {list(self.file1.columns)}")
                print(f"Available columns in file2: {list(self.file2.columns)}")
                return

            values = data_df[col_name].values
            expected_size = size_x * size_y
            if len(values) < expected_size:
                print(f"Not enough data points. Expected {expected_size}, got {len(values)}")
                return

            # Reshape to 2D array (y x x dimensions)
            image_data = values[:expected_size].reshape(size_y, size_x).copy()

            # Flip alternate rows left-to-right (rows 0, 2, 4, ...)
            image_data[::2] = np.flip(image_data[::2], axis=1)

            # Apply log scale if enabled
            if self.log_y.get():
                image_data = np.where(image_data > 0, np.log10(image_data), np.nan)

            # Compute 2.5th and 97.5th percentiles for color scaling
            finite_vals = image_data[np.isfinite(image_data)]
            if finite_vals.size > 0:
                vmin = np.percentile(finite_vals, 2.5)
                vmax = np.percentile(finite_vals, 97.5)
            else:
                vmin, vmax = None, None

            # Create a new figure window
            fig_window = plt.figure(figsize=(8, 8))
            ax = fig_window.add_subplot(111)
            im = ax.imshow(image_data, cmap='viridis', origin='upper', aspect='equal', vmin=vmin, vmax=vmax)
            ax.set_title(f"Pixel Map: {col_name}")
            ax.set_xlabel("X (pixels)")
            ax.set_ylabel("Y (pixels)")
            cbar = fig_window.colorbar(im, ax=ax)
            cbar.set_label(col_name)
            fig_window.tight_layout()
            plt.show()
            print(f"Pixel map generated for column '{col_name}'")
        except Exception as e:
            print(f"Failed to generate pixel map: {e}")
            import traceback
            traceback.print_exc()

# Run the application
root = tk.Tk()
app = DataPlotterApp(root)
root.mainloop()
