#%%

from cartooff import cartooff
import cartopy.crs as ccrs

longitude = 120, 150, 10        #? W, E, tick interval
latitude = 20, 50, 10           #? S, N, tick interval
resolution = '50m'              #? map resolution ...   '10m', '50m', '110m'

inset_extent = 138.1, 141.15, 34.6, 37.3    #? W, E, S, N

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

# 拡大図を図中に表示
# width:       全体図に対する縮小図の横幅の割合
# position:    全体図左下からの相対位置（横、縦）
# loc:         indicator の点線を出す頂点（右上から反時計回りに1, 2, 3, 4）
cf.add_inset_map(inset_extent, width=0.4, position=[0.5, 0.05])

cf.axin.add_feature(cf.countries, zorder=1)
# 関東地方の shape を取得
kanto = [cf.get_japan_shape('Ibaraki'), cf.get_japan_shape('Tochigi'), cf.get_japan_shape('Gunma'), cf.get_japan_shape('Saitama'), cf.get_japan_shape('Chiba'), cf.get_japan_shape('Tokyo'), cf.get_japan_shape('Kanagawa')]

for pref in kanto:
    # 拡大図の中に shape を追加する（target='inset'）
    cf.add_shape(pref, target='inset', facecolor='limegreen', edgecolor='dimgray')

# 図を表示して保存
cf.save('./example2.png')
cf.show()
# %%
