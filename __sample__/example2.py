#%%

from cartooff import cartooff
import cartopy.crs as ccrs

longitude = 120, 150, 10        #? W, E, tick interval
latitude = 20, 50, 10           #? S, N, tick interval
resolution = '50m'              #? map resolution ...   '10m', '50m', '110m'

# 東経160度を中心としたメルカトル図法のオブジェクトを作成
# 第一引数に cartopy.crs のクラスを渡し、第二引数以降でそのクラスの引数を設定できる
# 注意点として、デフォルトの正距円筒図法（PlateCaree）以外ではバグるので inset indicator が使えない。（メルカトルのような円筒図法だとしても）
cf = cartooff(ccrs.NearsidePerspective, central_longitude=135, central_latitude=30)

# ベースの地図を描画
colored_countries = {
    'Japan': 'palegreen',
}
cf.draw(longitude, latitude, resolution,
        lon_label=False, lat_label=False,
        colored_countries=colored_countries)

cf.save('./example2.png')
cf.show()
# %%
