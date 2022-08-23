#%%

from cartooff import cartooff

longitude = 100, 150, 10        #? W, E, tick interval
latitude = 15, 50, 10           #? S, N, tick interval
resolution = '50m'              #? map resolution ...   '10m', '50m', '110m'

inset_extent = 122.7, 124.5, 23.9, 24.7    #? W, E, S, N

# オブジェクトを作成
cf = cartooff()

# ベースの地図を描画
# 国別に色分けが可能。keyに国名、valに色名
colored_countries = {
    'Japan': 'palegreen',
}
cf.draw(longitude, latitude, resolution, colored_countries=colored_countries)

# 拡大図を図中に表示
# width:       全体図に対する縮小図の横幅の割合
# position:    全体図左下からの相対位置（横、縦）
# loc:         indicator の点線を出す頂点（右上から反時計回りに1, 2, 3, 4）
cf.add_inset_map(inset_extent, width=0.3, position=[0.6, 0.1], loc=[2,3])

# shape を取得して地図に描画する
# target='inset' にすると拡大図内にプロットできる
okinawa = cf.get_japan_shape('Okinawa')
cf.add_shape(okinawa, target='inset', facecolor='palegreen', edgecolor='black')

yonaguni = cf.get_japan_shape('Yonaguni Cho')
cf.add_shape(yonaguni, target='inset', facecolor='orange', edgecolor='black')

hateruma = cf.get_japan_shape('Taketomi Cho')
hateruma = hateruma[-1:] #? 波照間島は竹富町のShapeの最後
cf.add_shape(hateruma, target='inset', facecolor='tomato', edgecolor='black')

# csv を読み取って図中にプロット
# type 列に inset とすると拡大図に、map にすると外の図にプロット。
# point 列, label 列 でそれぞれを描画するか設定できる。
cf.plot_points('./example.csv')

# 図を保存する際、show() する前に save() と保存できない
cf.save('./example.png')
cf.show()
# %%
