# -*- coding: utf-8 -*-

import unittest
from nose.tools import eq_, ok_
from wiki_converter.log import create_logger
from wiki_converter.parser import PukiwikiParser
from wiki_converter.converter import ConfluecenConverter

class TestPukiwikiParser(unittest.TestCase):
    def setUp(self):
        self.log = create_logger(True)
        self.parser = PukiwikiParser(self.log)
        self.converter = ConfluecenConverter(self.log)

    def testHeading(self):
        self.converter.reset_converted_text()
        self.parser.parse_text(u"* ヘッディング1", self.converter)
        eq_(
            u"h2. ヘッディング1\n",
            self.converter.converted_text,
            'heading1'
        )
        
        self.converter.reset_converted_text()
        self.parser.parse_text(u"***ヘッディング3", self.converter)
        eq_(
            u"h4.ヘッディング3\n",
            self.converter.converted_text,
            'heading3'
        )

    def testToc(self):
        self.converter.reset_converted_text()
        self.parser.parse_text(u"#contents", self.converter)
        eq_(
            u"{toc}\n",
            self.converter.converted_text,
            'toc'
        )

    def testTableColumns(self):
        self.converter.reset_converted_text()
        self.parser.parse_text(u"| ほげ | ふが |", self.converter)
        eq_(
            u"| ほげ | ふが |\n",
            self.converter.converted_text,
            'table_columns'
        )

    def testHeaderTableColumns(self):
        self.converter.reset_converted_text()
        self.parser.parse_text(u"| これは | ヘッダー |h", self.converter)
        eq_(
            u"|| これは || ヘッダー ||\n",
            self.converter.converted_text,
            'table_header_columns'
        )

    def testTable(self):
        self.converter.reset_converted_text()
        self.parser.parse_text("""\
| num | text |h
| 1 | one |
""".rstrip(), self.converter)

        eq_("""\
|| num || text ||
| 1 | one |
""".rstrip(),
            self.converter.converted_text.rstrip(),
            'table_header_columns'
        )

    def testFormattedText(self):
        self.converter.reset_converted_text()
        self.parser.parse_text(u"""\
 This is a
 formatted
 text.
""".rstrip(), self.converter)
        print self.converter.converted_text
        eq_("""\
{code}
This is a
formatted
text.
{code}
""".rstrip(),
            self.converter.converted_text.rstrip(),
            'formatted_text'
        )

    def testItalic(self):
        self.converter.reset_converted_text()
        self.parser.parse_text(u"'''Italic text.''' Normal text.", self.converter)
        self.log.debug("converted : `%s`" % self.converter.converted_text)
        eq_(
            u"_Italic text._ Normal text.",
            self.converter.converted_text,
            'italic'
        )

    def testStrong(self):
        self.converter.reset_converted_text()
        self.parser.parse_text(u"''Strong text.'' Normal text.", self.converter)
        self.log.debug("converted : `%s`" % self.converter.converted_text)
        eq_(
            u"*Strong text.* Normal text.",
            self.converter.converted_text,
            'strong'
        )

    def testLink(self):
        self.converter.reset_converted_text()
        self.parser.parse_text(u"[[リンクテスト|http://www.ameba.jp]]", self.converter)
        self.log.debug("converted : `%s`" % self.converter.converted_text)
        eq_(
            u"[リンクテスト|http//www.ameba.jp]",
            self.converter.converted_text,
            'link'
        )

        self.converter.reset_converted_text()
        self.parser.parse_text(u"[[LinkPage]]", self.converter)
        self.log.debug("converted : `%s`" % self.converter.converted_text)
        eq_(
            u"[LinkPage]",
            self.converter.converted_text,
            'link'
        )


    def testList(self):
        self.converter.reset_converted_text()
        self.parser.parse_text(u"""\
- bullet1
-- bullet2
-+ bullet + number1
-+ bullet + number2
+ number1
""", self.converter)

        self.log.debug("converted : {%s}" % self.converter.converted_text)
        eq_(u"""\
* bullet1
** bullet2
*# bullet + number1
*# bullet + number2
# number1
""".rstrip(),
            self.converter.converted_text.rstrip(),
            'list'
        )

#    def testComplex(self):
#        self.converter.reset_converted_text()
#        self.parser.parse_text(
#            u"""
#* タイトル
#''強調'' ほげほげ
#""",
#            self.converter)
#        print "converted : {%s}" % self.converter.converted_text

#    def testComplex2(self):
#        self.converter.reset_converted_text()
#        self.parser.parse_text(u"""\
#[[システム]]
#
##contents
#
#* 今月のダウンタイム [#w206e904]
#
#| 月 | PC | MB | SP |h
#| 10月 | 4.75 | 0 | 0 |
#| 9月 | 0 | 0 | 0 |
#| 8月 | 0 | 0.25 | 0 |
#| 7月 | 2.75 | 0 | 1.5 |
#| 6月 | 1.25  | 0 | 0 |
#
#* Redmineのチケット一覧 [#r1260668]
#http://172.22.109.44:3000/issues?query_id=16
#
#* 進行中のプロジェクト [#p45ba321]
#
#** 代官山の回線増設(NWチーム、並河) [#u0f1f697]
#
#** LVS置き換え(NWチーム、並河) [#h471c446]
#
#** DB/memcached/Isilonへのアクセス制限入れる(並河) [#q95205b1]
#本番環境のサーバからのみアクセスできるようにする。
#
#** WAP増設(並河、生沼) [#k1159a03]
#
#** info増設(並河、生沼) [#b657a04a]
#
#** chat増設(並河、生沼) [#j2fd7eb2]
#
#** game増設(並河、生沼) [#hd2f4e4c]
#
#** Isilonのピグパーツ情報のバックアップ(生沼) [#e6acd48f]
#アイシロンのデータをバックアップする、かつ容量を見極める。
#
#*** 9/21 [#mf7b774c]
#- 障害対応などで進まず
#
#
#** MySQLマスタ障害時のフェイルオーバー(桑野) [#m42bfe72]
#MHA使うなどして、マスタ障害発生時のダウンタイムを少なくしたい for 品質向上キャンペーン
#
#** IsilonをWebDAV的なものにリプレース [#s270aa97]
#
#
#** バッチ(Hadoop使用)がOOMで落ちる(生沼) [#ad6a5473]
#- Hadoopでreduceしている時にNodeのheapサイズ以上のデータを処理しようとしてOOMで落ちることがここ最近(2週間で1回ぐらい)発生している
#- そろそろ限界な予感がするので、詳細を調査した上で下記の対応する。
#--Hadoopクラスタごと置き換える(Nodeサーバのスケールアップ)
#--解析プログラムを何とかする
#
#*** 7/27 [#f2ed278e]
#- 進捗なし
#
#** Apacheバージョンアップ(大田) [#e0fa0c2a]
#
#**Tomcatバージョンアップ(大田) [#r86d4540]
#
#6系の最新にする。合わせてcommon-tomcat のRPMにする。
#
#** JDKバージョンアップ(大田) [#ff081b96]
#common-jdkにする。WAPはTomcatをcommonにすれば自動的に変わるので、ソケットサーバのものを変える。
#
#** dev,stgのuserIdを10億番台にする（有馬） [#la81d9b1]
#- 個人devで検証準備中
#- 11/14週よりdev,stgで実施予定
#
#** profileAPIの向き先変更（有馬） [#cebd36b0]
#- 11/16より順次移行予定
#
#** サーバ応答速度の可視化（有馬） [#wfa1c60a]
#- muninのグラフに以下を追加する
#-- wapのレスポンス平均
#-- socketへのコマンド処理時間平均、コマンド回数
#-- dbのslowQuery
#-- など
#
#** パフォーマンスチューニング（有馬） [#n34c15ea]
#- loadBulk時にキャッシュにのせる
#-- loadBulkで、DBから取得したデータを、キャッシュにセットしていないのが発覚したのでその対応
#-- コードレビュー中。11/15リリース予定。
#
#** MySQLを5.1にバージョンアップ [#tf195ec9]
#*** 7/21 [#bf654918]
#- 凖環境にFIO差してもらう
#- RPMは本家の最新のものを使う
#
#*** 7/13 [#d2cec84d]
#- FusionIOを凖環境にさす。来週中
#- Staging,Devは5.1に先行してバージョンアップするので、RPMもらう
#
#* 今週のwarn分析 [#f8acdeb6]
#
#http://172.28.202.61/MailCheck_ver2/entry.html
#
#ワンライナー書いて集計したぜ！
#- [[個人/並河祐貴/warn分析]]
#
#* そのうちやるもの [#ef24ec51]
#
#** ディプロイスクリプト改善 [#s7b75100]
#
#ナイトホークをやるにあたって、個人Dev/Dev/Staging/本番で全て共通で使えるようなディプロイスクリプトを作る。
#
#** Tomcatの停止方法改善 [#v0e4c7f5]
#現状
#
# kill -9 <pid>
#
#でTomcatをシャットダウンしているので、これを改善する。spymemcachedが悪さをしているらしい。https://groups.google.com/forum/#!topic/spymemcached/lMpHWENfKEE
#
#
#** NEW:コマンド制限の改善 [#zf9a877c]
#内容：http://amewiki.cadc.cyberagent.local/pages/viewpage.action?pageId=5177837
#
#
#
#** FusionIOのファームアップデート(桑野) [#v944ddb0]
#statusを取るときのロックが無くなっているらしい。
#
#** アイテムリリース光速化(未定) [#n0ba4fa5]
#
#** NEW:IPが取れないコマンド連発されたら接続断(未定) [#ef1318e4]
#
#** NEW:wapボトルネック調査＆改善(未定) [#fc4ffd09]
#- /core/swf/thumbnail/userの304対応後、まだWAPの負荷が高い場合は根本的な原因を調査する
#- アプリを直すことで改善できるのであれば直す
#- WAPはとにかく台数が多くなってしまうので、ボトルネック調べてアプリのチューニングでさくっと負荷減らせそうだったら対応したい
#
#** NEW:wapリプレース(未定) [#vef4af76]
#キャパプラ含めて検討する。
#- たとえばCPUコアを倍、メモリを倍にした場合に倍の性能が出るのか？＝スケールアップすれば台数減らせるのか？
#- 上記の「wapボトルネック調査＆改善」をやってから行う
#-- 例えばIsilonが原因の場合はスケールアップしても改善しない可能性が高いので。
#
#
#** NEW:lockサーバリプレース(未定) [#n54ba73e]
#ミルフィーユ→1Uにしてスケールアップし台数を減らす。
#
#
#** NEW:ソケットサーバ負荷試験環境構築(未定) [#f273e16b]
#1台だけでもいいので、新しく実装したコマンドの負荷テストができるようにする。
#
#** NEW:Isilon置き換える(未定) [#gedea485]
#
#
#** WAPに大量のリクエストが来た場合にはじく対策(並河) [#ab036d92]
#- イベント機能の障害の再発防止策
#
#** Dev,StagingのWAPにLVSを導入(並河) [#rc293e87]
#
#** source ipが取れないような不正なコマンドをBAN [#ka67b154]
#https://172.28.139.109/ameba_event_watchdog_admin/event/detail?eventId=15
#の再発防止策。
#
#** WAPで配信しているdatファイルキャッシュ効いてないよ(生沼) [#v9c0757d]
#- クライアント側の実装を確認(生沼)
#
#*** 4/15 [#o4a1df8f]
#- Flashの設定をかえたらきゃっしゅされた？要確認(生沼)
#
#*** 3/18 [#z0e2358b]
#- アイテムの運用方法(なにか修正があったらアイテムコードを新しくするか)を小針さんに確認する(生沼)
#
#*** 3/10 [#zf730a61]
#- 並河さんにバトンタッチ
#
#** NEW:汎用MQシステム構築と既存通知処理の置き換え(生沼) [#m8718293]
#- 「ピグともがオンラインになりました」
#- 「手紙が届いています」
#
#などの通知系は、現状ソケットサーバ同士で接続して通知処理を行っているが、ソケットサーバがダウンしている場合に処理が詰まってしまうので、間にMQサーバを立ててそこから通知するようにしたい。
#
#MQサーバの冗長化どうすんの？っていう話はあるけど...
#
#** Muninリプレース [#q6fa0264]
#- Muninはサーバの台数が多いと顕著にパフォーマンス劣化する。
#- ピグの場合、5分に1回更新されるはずのグラフが15分経たないと更新されない
#- 5分おきに更新されないトレンド監視ツールはあまり意味が無いので、GangliaとかCloudForecastとか、大量のサーバでも大丈夫なものに置き換えたい
#- もしくはMuninを高速化できるんだったらそれでもおｋ
#
#* 終わったタスク [#iea5c2a8]
#[[システム/コアシス定例MTG/終わったタスク]]を参照。
#
#* 過去ログ [#ke03b0db]
#
##lsx(システム/コアシス定例MTG/,reverse=true)
#""",
#            self.converter)
#        
#        self.log.debug("----------------------------------")
#        self.log.debug("converted : `%s`" % self.converter.converted_text)
#        eq_(
#            u"",
#            self.converter.converted_text,
#            'complex2'
#        )
