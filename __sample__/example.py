#%%

from cartooff import cartooff

longitude = 100, 150, 10        #? W, E, tick interval
latitude = 15, 50, 10           #? S, N, tick interval
resolution = '50m'              #? map resolution ...   '10m', '50m', '110m'

# オブジェクトを作成
cf = cartooff()

# ベースの地図を描画
# 国別に色分けが可能。keyに国名、valに色名
colored_countries = {
    'Japan': 'palegreen',
}
cf.draw(longitude, latitude, resolution, colored_countries=colored_countries)

# 図を保存する際、show() する前に save() と保存できない
cf.save('./example.png')
cf.show()
# %%
