# [[ cartooff.py ]]

# To set up the environment, execute the following commands first.
# $ conda env create -f=environments.yml
# $ conda activate cartopy

# >>>>>>>>>> Import >>>>>>>>>>
import os
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patheffects import withStroke
import matplotlib.ticker as mticker
import cartopy
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LatitudeFormatter,LongitudeFormatter
import cartopy.feature as cfeature
from cartopy.feature import ShapelyFeature
import cartopy.io.shapereader as shapereader
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset
from shapely.geometry.polygon import LinearRing
# <<<<<<<<<< Import <<<<<<<<<<

class ProccessError(Exception):
    pass

class cartooff:
    def __init__(self, proj=ccrs.PlateCarree, **kwargs):
        self.proj_class = proj
        self.proj = ccrs.PlateCarree()
        obj = proj(**kwargs)
        self.fig = plt.figure(figsize=(336/25.4, 240/25.4), dpi=200, facecolor='w')
        self.ax = self.fig.add_subplot(111, projection=obj)
        plt.rcParams['font.size']=20
        plt.rcParams['font.family']='sans-serif'
        self.shown = False

    def draw(self, longitude, latitude, resolution='50m',
            land_color=cfeature.COLORS['land'],
            ocean_color=cfeature.COLORS['water'], colored_countries=dict(), coastlines=True, country_border=True, gridlines=True,
            lon_label=True, lat_label=True):
        self.longitude = longitude
        self.latitude = latitude
        self.resolution = resolution

        #! shape datas
        self.land  = cfeature.NaturalEarthFeature('physical', 'land', resolution,
            edgecolor='face', facecolor=land_color)
        self.ocean = cfeature.NaturalEarthFeature('physical', 'ocean', resolution,
            edgecolor='face', facecolor=ocean_color)
        self.countries  = cfeature.NaturalEarthFeature('cultural', 'admin_0_countries', resolution,
            edgecolor='gray', facecolor='none')

        shape_countries_path = shapereader.natural_earth(resolution=resolution,
            category='cultural', name='admin_0_countries')
        shape_countries = shapereader.Reader(shape_countries_path)

        self.shape_japan_highresol = shapereader.Reader(os.path.dirname(__file__)+'/data/polbnda_jpn.shp')

        self.colored_countries = []
        for country, color in colored_countries.items():
            shape = ShapelyFeature([x.geometry for x in list(filter(lambda c: country in c.attributes['NAME'], shape_countries.records()))][0],
                        self.proj, facecolor=color, edgecolor='none')
            self.colored_countries.append(shape)
            if country == 'Japan' and resolution in ['10m', '50m']:
                #? NaturalEarth だと北方領土がロシア領扱いされているので、日本として描画
                hoppo_ryodo_cities = ['shikotan-mura', 'Shikotan Mura', 'Tomari Mura', 'Ruyabetsu Mura', 'Rubetsu Mura', 'Shana Mura', 'Shibetoro Mura']
                self.geometries_japan = ShapelyFeature(self.shape_japan_highresol.geometries(), self.proj, facecolor=color, edgecolor='none')
                geometries_hoppo_ryodo = [x.geometry for x in list(filter(lambda c: c.attributes['laa'] in hoppo_ryodo_cities, self.shape_japan_highresol.records()))]
                hoppoRyodo = ShapelyFeature(geometries_hoppo_ryodo, self.proj, facecolor=color, edgecolor='none')
                self.colored_countries.append(hoppoRyodo)

        #! axis settings
        self.ax.set_extent([longitude[0], longitude[1], latitude[0], latitude[1]], crs=self.proj)
        lonfmt = LongitudeFormatter(zero_direction_label=True)
        latfmt = LatitudeFormatter()
        self.ax.xaxis.set_major_formatter(lonfmt)
        self.ax.yaxis.set_major_formatter(latfmt)
        lon_dist = longitude[1] - longitude[0]
        lat_dist = latitude[1] - latitude[0]
        lon_order = self.get_num_order(longitude[2])
        lat_order = self.get_num_order(latitude[2])
        lon_min = math.ceil(longitude[0] / 10 ** lon_order) * 10 ** lon_order
        lat_min = math.ceil(latitude[0] / 10 ** lat_order) * 10 ** lat_order
        lon_ticks = np.arange(lon_min, longitude[1]+1, longitude[2])
        lat_ticks = np.arange(lat_min, latitude[1]+1, latitude[2])
        lon_ticks = [self.lon_tick_limitter(x) for x in lon_ticks]
        lat_ticks = [self.lat_tick_limitter(x) for x in lat_ticks]
        if lon_label:
            self.ax.set_xticks(lon_ticks, crs=self.proj)
            self.ax.set_xlabel('Longitude', fontsize=24)
            self.ax.tick_params(axis='x', labelsize=20)
        if lat_label:
            self.ax.set_yticks(lat_ticks, crs=self.proj)
            self.ax.set_ylabel('Latitude', fontsize=24)
            self.ax.tick_params(axis='y', labelsize=20)

        self.lon_dist = lon_dist
        self.lat_dist = lat_dist
        self.dist_scale = min(self.lon_dist, self.lat_dist)

        #! plot maps
        self.ax.add_feature(self.ocean, zorder=1)
        self.ax.add_feature(self.land, zorder=2)
        if country_border:
            self.ax.add_feature(self.countries, zorder=3)
        for gm in self.colored_countries:
            self.ax.add_feature(gm, zorder=4)
        if coastlines:
            self.ax.coastlines(resolution=resolution, zorder=5)
        if gridlines:
            gl = self.ax.gridlines(crs=self.proj, draw_labels=False,
                color='black', linewidth=0.5, linestyle=':')
            gl.xlocator = mticker.FixedLocator(lon_ticks)
            gl.ylocator = mticker.FixedLocator(lat_ticks)

    def lon_tick_limitter(self, x):
        return x - 360 if x > 180 else x

    def lat_tick_limitter(self, x):
        return x - 180 if x > 90 else x + 180 if x < -90 else x

    def get_japan_shape(self, name=''):
        if name == '':
            return [x.geometry for x in self.shape_japan_highresol.records()]
        else:
            return [x.geometry for x in list(filter(lambda c: name in c.attributes['laa'] or name in c.attributes['nam'],
            self.shape_japan_highresol.records()))]

    def add_shape(self, shape, target='outset', facecolor='tomato', edgecolor='black', zorder=2):
        if isinstance(shape, list):
            feature = ShapelyFeature(shape, self.proj, facecolor=facecolor, edgecolor=edgecolor)
            if target == 'inset':
                self.axin.add_feature(feature, zorder=zorder)
            else:
                self.axin.add_feature(feature, zorder=zorder)
        else:
            if target == 'inset':
                self.axin.add_feature(shape, zorder=zorder)
            else:
                self.ax.add_feature(shape, zorder=zorder)

    def plot_points(self, filepath):
        df = pd.read_csv(filepath, encoding='utf-8')
        for i, row in df.iterrows():
            if row['type'] == 'inset':
                if row['point']:
                    self.axin.scatter(row.lon, row.lat, c='lightgray', marker='o',
                        linewidths=2, edgecolors='gray',
                        s=100, transform=self.proj, zorder=10)
                if row['label']:
                    self.axin.text(row.lon+self.axin_dist_scale/75, row.lat+self.axin_dist_scale/75, row.label,
                        path_effects=[withStroke(linewidth=3, foreground="#ffffff")],
                        transform=self.proj, zorder=11)
            else:
                if row['point']:
                    self.ax.scatter(row.lon, row.lat, c='lightgray', marker='o',
                        linewidths=2, edgecolors='gray',
                        s=100, transform=self.proj, zorder=10)
                if row['label']:
                    self.ax.text(row.lon+self.dist_scale/75, row.lat+self.dist_scale/75, row.label,
                        path_effects=[withStroke(linewidth=3, foreground="#ffffff")],
                        transform=self.proj, zorder=11)

    def add_inset_map(self, inset_extent, width=0.3, position=[0,0], indicator=True,
            loc=[2,3], bgcolor='white', edgecolor='red'):
        self.axin_w, self.axin_e, self.axin_s, self.axin_n = inset_extent
        self.axin_lon_dist = self.axin_e - self.axin_w
        self.axin_lat_dist = self.axin_n - self.axin_s
        axin_aspect = self.axin_lat_dist / self.axin_lon_dist
        ax_aspect = self.lat_dist / self.lon_dist
        self.axin_y_scale = axin_aspect / ax_aspect
        self.axin_width = int(width*100)/100
        self.axin_height = width*self.axin_y_scale

        self.axin_dist_scale = min(self.axin_e-self.axin_w, self.axin_n-self.axin_s)
        self.axin = inset_axes(self.ax, width=f"{self.axin_width*100}%", height=f"{self.axin_height*100}%", loc='lower left', borderpad=0,
            bbox_to_anchor=(position[0], position[1], 1, 1), bbox_transform=self.ax.transAxes,
            axes_class=cartopy.mpl.geoaxes.GeoAxes,
            axes_kwargs=dict(map_projection=self.proj, aspect='equal'))
        self.axin.set_xlim(self.axin_w, self.axin_e)
        self.axin.set_ylim(self.axin_s, self.axin_n)
        self.axin.axis('off')

        nvert = 100
        areaIndicate_lon = np.r_[np.linspace(self.axin_w, self.axin_w, nvert),
                np.linspace(self.axin_w, self.axin_e, nvert),
                np.linspace(self.axin_e, self.axin_e, nvert)].tolist()
        areaIndicate_lat = np.r_[np.linspace(self.axin_s, self.axin_n, nvert),
                np.linspace(self.axin_n, self.axin_n, nvert),
                np.linspace(self.axin_n, self.axin_s, nvert)].tolist()
        areaIndicator = LinearRing(list(zip(areaIndicate_lon, areaIndicate_lat)))
        self.areaIndicator = areaIndicator
        self.ax.add_geometries([areaIndicator], self.proj,
                facecolor='none', edgecolor=edgecolor, linewidth=1, zorder=6)
        self.axin.add_geometries([areaIndicator], self.proj,
                facecolor=bgcolor, edgecolor='none', linewidth=3, zorder=1)
        self.axin.add_geometries([areaIndicator], self.proj,
                facecolor='none', edgecolor=edgecolor, linewidth=3, zorder=100)

        if indicator and self.proj_class == ccrs.PlateCarree:
            mark_inset(self.ax, self.axin, loc1=loc[0], loc2=loc[1], edgecolor=edgecolor, linewidth=0.8, linestyle='--')

    def save(self, filename):
        if self.shown:
            raise ProccessError('The figure must be saved before it is showed.')
        else:
            plt.savefig(filename, bbox_inches="tight", pad_inches=0.05)
            self.saved = True

    def show(self):
        plt.show()
        self.shown = True

    def is_num(self, s):
        try:
            float(s)
        except ValueError:
            return False
        else:
            return True

    def get_num_order(self, x):
        head_flg = 0
        period_flg = 0
        order = 0
        x_str = f'{x:f}'

        if x_str[0] == '-':
            x_str = x_str[1:]
        for c in x_str:
            assert self.is_num(c) or c == '.', f'Unexpected character: {c}'
            if not period_flg:
                if head_flg:
                    if c == '.':
                        return order
                    else:
                        order += 1
                else:
                    if c == '.':
                        period_flg = 1
                    elif not c == '0':
                        head_flg = 1
            else:
                assert not c == '.', 'Duplicate periods.'
                order -= 1
                if not c == '0':
                    return order
        if head_flg:
            return order
        else:
            return 0