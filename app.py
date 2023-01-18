#ライブラリのインポート
from PIL import Image
from telnetlib import RCP
import streamlit as st
import math

#画像生成
image1,image2 = st.columns(2)
with image1:
   image1 = Image.open('1124_s.jpg')
    
with image2:
   image2 = Image.open('1124_s.jpg')

#スライダー生成及び範囲設定
sl = st.slider('θ値', min_value=1,max_value=45)

#スライダーの値が変化したときの処理
if sl:
    #元画像の高さ，幅の情報を得る
    height = image1.height
    width = image1.width
    #元画像の座標4点を算出
    src = (0, 0, 
           0,height,
           width, height, 
           width, 0)
    k = sl
    k2 = math.radians(k) #スライダーの値をラジアンに変換
    c = 3.25 #両目の視差
    b = c / k2 #左目用と右目用の画像を生成するため，両目の視差を半分の値にする
    a = math.sqrt(b**2 + c**2) #画面と対象物の距離の算出

    d = 30 #画面と目の距離
    ppi = 300 #画像の解像度設定
    ppc = ppi / 2.54 #ピクセルの値をcmの値に変換
 
    wid = width * b / a #加工画像の移動距離の算出
    x = height / (1 + width * c / a / (d * ppc)) #画面上の加工画像の高さを算出

    #元画像から加工画像の変化量を算出
    h = (height - x) / 2 
    y1 = h
    y2 = height - h
    wx = width - wid

    #左目用の加工画像の4点座標を決める
    tarl = (wx, y1, 
        wx, y2,
        width, height, 
        width, 0
    )
        
    #右目用の加工画像の4点座標を決める  
    tarr = (0, 0, 
        0, height, 
        wid, y2, 
        wid, y1
    )

    #左目用の画像を射影変換
    im1 = image1.transform(
        size=(width,height),
        method=Image.QUAD,
        data=tarl,
        resample=Image.BICUBIC
    )

    #右目用の画像を射影変換
    im2 = image2.transform(
        size=(width,height),
        method=Image.QUAD,
        data=tarr,
        resample=Image.BICUBIC
    )

    #加工した左右の画像2枚を1枚にする
    dst = Image.new(mode='RGB', size=(im1.width + im2.width, max(im1.height, im2.height)))
    dst.paste(im1, box=(0, 0))
    dst.paste(im2, box=(im1.width, 0))

    #画像表示
    st.image(dst)
