# WanImageToVideo_Simpler

このカスタムノードは、従来の WanImageToVideoをアップデートし、**入力部を1つに減らす・ウェイトをッ加える**機能を追加したバージョンです。  


入力部を1つに減らすことで、処理時間を軽減することができます。


FLUXやHunyuanVideoと同様にadvanced custum samplerで生成することができます。


---
## スクリーンショット

下記のように、Input部がpotiveのみになり、conditioningとclipvisionのウェイトを設定できます。


![WanImageToVideo](https://github.com/Shiba-2-shiba/WanImageToVideoSimpler/blob/main/img1.png)


## Install


以下のコマンドでインストール出来ます。

You can install it with the following command.


```bash
cd Yourdirectory/ComfyUI/custom_nodes
git clone https://github.com/Shiba-2-shiba/WanImageToVideoSimpler.git

```

## Usage

ワークフローで、使用例を提示しています。使用している画像もwebp画像としてアップロードしています。

以下の記事で経緯や使用方法について記載していますので参考にしてください。

https://note.com/gentle_murre488/n/n81177ffc530b


---
## Reference Script
以下のスクリプトを参考にしています。

This custom node is based on the following script.

https://github.com/comfyanonymous/ComfyUI/blob/master/comfy_extras/nodes_wan.py
