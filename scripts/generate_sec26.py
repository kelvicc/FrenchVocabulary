# -*- coding: utf-8 -*-
"""
Generate Section 26 strictly adhering to original DUO 3.0 Section 26 (Sentences 302-311 -> No. 294-303).
"""
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECTIONS_DIR = os.path.join(BASE_DIR, 'sections')

content = """# Section 26 — 交通機関・宿泊施設・施設マナー・外食とレストラン・有名人とファン (No. 294 – No. 303)

### No. 294 [♂ Remy]
> **« Pardon, à quelle fréquence les navettes circulent-elles vers le centre-ville ? »**
> （すみません、市街地（中心街）行きのシャトルバスはどのくらいの間隔で運行していますか？）

- **1157 | à quelle fréquence** `/a kɛl fʁe.kɑ̃s/` 【副句】 どのくらいの頻度で，どれくらいの間隔で
  - (= **tous les combien** [どのくらいおきに], **combien de fois par...**)
  - ※ 【疑問表現の急所】英語の *how often* にあたる論理的で明快な表現。日常会話では *tous les combien* も頻用される（*Les bus passent tous les combien ?*：バスは何分おきに出ますか？）。
  - □ **la fréquence** `/fʁe.kɑ̃s/` 【名・女】 頻度；（物理）周波数
  - □ **fréquent(e)** `/fʁe.kɑ̃, -t/` 【形】 頻繁な，よくある
  - □ **fréquemment** `/fʁe.ka.mɑ̃/` 【副】 頻繁に，しばしば
- **1158 | une navette** `/na.vɛt/` 【名・女】 シャトルバス，定期往復便；（機織りの）杼（ひ）
  - (= **le bus de liaison** [連絡バス])
  - ※ 【交通用語】空港と駅、ホテルと中心街を結ぶ定期ピストン輸送便。宇宙船の「スペースシャトル」も *la navette spatiale*。成句 **faire la navette** で「（職場や学校へ）毎日往復通勤・通学する（= commute）」を表す。
- **1159 | circuler** `/siʁ.ky.le/` 【自】 ①（車両・便が）運行する，走る ②（人・血液・情報が）循環する，行き交う
  - (= **rouler** [走る], **fonctionner** [運行する])
  - ※ 【交通と循環】*Les trains circulent normalement.*（列車は平常通り運行しています）。交通整理の警官の *« Circulez ! »* は「立ち止まらないで進んでください！」。
  - □ **la circulation** `/siʁ.ky.la.sjɔ̃/` 【名・女】 交通，往来；循環 (*les embouteillages / la circulation dense*：渋滞)
- **1160 | le centre-ville** `/sɑ̃.tʁə.vil/` 【名・男】 市街地，中心街，ダウンタウン
  - (= **le cœur de la ville**, **les quartiers centraux**)
  - ※ 【冠詞と前置詞】無冠詞前置詞句 **en centre-ville**（中心街で／へ）としても頻出。郊外（*la banlieue*）と対比される。複数形は *les centres-villes*。

---

### No. 295 [♀ Denise]
> **« Ce motel est en mesure de loger jusqu'à quatre cents personnes. »**
> （そのモーテル（宿泊施設）は、400人もの宿泊客を収容することができます。）

- **1161 | le motel** `/mɔ.tɛl/` 【名・男】 モーテル，自動車旅行者用ホテル
  - (= **l'hôtel routier**)
  - ※ 【語源】*motor* + *hotel* からなる英語借用語。幹線道路沿いにある駐車場直結の宿泊施設。
- **1162 | être en mesure de (+ inf.)** `/ɛtʁ ɑ̃ mə.zyʁ də/` 【成句】 〜することができる，〜できる立場にある
  - (= **être capable de** [〜する能力がある], **être à même de**, **pouvoir**)
  - ※ 【公的・ビジネス構文】単なる *pouvoir* よりも一段と改まった響きを持ち、十分な能力・設備・権限を備えていることを表す（= be in a position to / be capable of）。
  - □ **la mesure** `/mə.zyʁ/` 【名・女】 測定；基準；措置，対策 (*prendre des mesures*：対策を講じる)
- **1163 | loger** `/lɔ.ʒe/` 【他】 宿泊させる，収容する，住まわせる；【自】宿泊する，下宿する
  - (= **héberger** [泊める], **accueillir** [収容する], **abriter**)
  - ※ 【英語 accommodate に直結】客や家族に「寝泊まりする部屋を提供する」基幹動詞。*nourri et logé*（食事と部屋付きで）。
  - □ **le logement** `/lɔʒ.mɑ̃/` 【名・男】 住居，住宅，宿 (*la crise du logement*：住宅危機)
- **1164 | jusqu'à** `/ʒys.ka/` 【前】 ①（数量の極限）…もの，最大…まで ②（時間・空間）…まで
  - (= **pas moins de** […もの], **au maximum**)
  - ※ 【数量の強調】英語の *as many/much as...* や *up to...* に相当し、達する上限の大きさ・驚きを強調する。母音の前では *jusqu'à*、子音の前でも *à* を伴う（*jusqu'à dix heures*）。

---

### No. 296 [♀ Vivienne]
> **« Cette suite est trois fois plus spacieuse que mon appartement en copropriété. »**
> （このスイートルームは、私の分譲マンションの3倍の広さがある。）

- **1165 | une suite** `/sɥit/` 【名・女】 ①（ホテルの）続き部屋，スイートルーム ②続き，連続
  - (= **l'appartement d'hôtel**)
  - ※ 【ホテルの用語】リビングや寝室がひと続きになった豪華な客室（*la suite présidentielle*：プレジデンシャル・スイート）。
- **1166 | trois fois plus ... que** `/tʁwa fwa ply ... kə/` 【構文】 〜の3倍…である
  - (= **le triple de**)
  - ※ 【倍数比較の急所】*X fois plus + 形容詞/副詞 + que* で「〜のX倍…である」という倍数比較の標準定型構文（2倍なら *deux fois plus...*）。
- **1167 | spacieux(-euse)** `/spa.sjø, -øz/` 【形】 （部屋・家が）広々とした，ゆったりした
  - (= **vaste** [広大な], **large** [広い], **grand(e)**)
  - ※ 【不動産の核心語】ラテン語 *spatium*（空間・広がり）に由来。居住空間が狭苦しくなく開放的である様を賞賛する形容詞。
  - (↔ exigu(-uë) 狭苦しい，étroit(e) 狭い)
  - □ **l'espace** `/ɛs.pas/` 【名・男】 空間，宇宙
- **1168 | un appartement** `/a.paʁ.tə.mɑ̃/` 【名・男】 アパルトマン，マンション，住居
  - (= **le logement**, **l'habitation**)
  - ※ 【文化と語法】フランスでは都市部住民の大多数が集合住宅の「アパルトマン」に住む。日本の「アパート（木造賃貸）」と異なり、石造りの豪邸から近代高層まで集合住宅の一室全般を指す。
- **1169 | la copropriété** `/kɔ.pʁɔ.pʁi.je.te/` 【名・女】 （マンションの）区分所有，共同所有；区分所有建物
  - (= **la propriété collective**)
  - ※ 【英語 condominium の対応語】各住戸を個別に所有し共有部分を共同管理する形態。*un appartement en copropriété* で「分譲マンションの一室」。

---

### No. 297 [♂ Henri]
> **« Jeter des ordures dans cet établissement est passible d'une amende maximale de cinq cents euros. »**
> （この施設内でのゴミの投棄（ポイ捨て）は、最高500ユーロの罰金に処される可能性があります。）

- **1170 | les ordures** `/ɔʁ.dyʁ/` 【名・女・複】 （家庭・街頭の）ゴミ，生ゴミ，廃棄物
  - (= **les déchets** [廃棄物], **les détritus** [ゴミくず])
  - ※ 【日常最頻出】街頭のゴミ収集車は *le camion à ordures / la benne à ordures*。比喩的に人間に対して罵倒語（*Espèce d'ordure !*：クズ野郎！）としても用いられる。
- **1171 | un établissement** `/e.ta.blis.mɑ̃/` 【名・男】 ①施設，機関，事業所，学校 ②設立，制定
  - (= **l'institution**, **le bâtiment**, **l'organisme**)
  - ※ 【法律・公的用語】公共施設（*un établissement public*）や教育機関、営業所・ホテルなど、特定の社会的活動を行う建物を広く指す。
  - □ **établir** `/e.ta.bliʁ/` 【他】 設立する，確立する，制定する
- **1172 | passible de** `/pa.sibl də/` 【形】 （刑罰・罰金を）科される可能性がある，〜に処すべき
  - (= **exposé(e) à une peine de**)
  - ※ 【公的掲示の定番】法律・規程違反で「〜の刑に処せられる」ことを警告する硬い法律形容詞。*passible de deux ans de prison*（2年の禁錮刑の対象となる）。
- **1173 | une amende** `/a.mɑ̃d/` 【名・女】 罰金，過料
  - (= **la contravention** [交通違反などの反則金])
  - ※ 【同音異義語の罠】果物の「アーモンド（*l'amande*）」と同音！罰金は **amende** と綴る。成句 **faire amende honorable** は「公に謝罪して過ちを認める」。
- **1174 | maximal(e)** `/mak.si.mal/` 【形】 最大限の，最高（限度）の (※男複: *-maux*)
  - (= **le/la plus élevé(e)**)
  - ※ 【対比】*la vitesse maximale autorisée*（最高制限速度）。
  - (↔ minimal(e) 最小限の)
  - □ **le maximum** `/mak.si.mɔm/` 【名・男】 最大限，最高値

---

### No. 298 [♀ Vivienne]
> **« Ce restaurant est toujours plein à craquer ; il vaut mieux réserver au préalable. »**
> （あのレストランはいつも超満員よ。あらかじめ予約しておいたほうがいいわ。）

- **1175 | plein(e) à craquer** `/plɛ̃ a kʁa.ke/` 【成句】 （会場・店・乗り物が）超満員の，すし詰めの，破裂しそうなほどいっぱいの
  - (= **bondé(e)** [超満員の], **comble** [満席の])
  - ※ 【生き生きとした口語表現】直訳「きしむ（*craquer*）ほど満杯の」。客がぎっしり詰まった飲食店や満員電車を活写する定番表現。英語の *packed* に完全対応。
  - □ **craquer** `/kʁa.ke/` 【自】 パキッと音を立てる；（精神的に）耐えきれなくなる，キレる
- **1176 | il vaut mieux (+ inf.)** `/il vo mjø/` 【成句】 〜するほうがよい，〜したほうが賢明である
  - (= **il est préférable de**, **on ferait mieux de**)
  - ※ 【助言の超重要構文】動詞 *valoir* の非人称構文。相手に行動を促す際、英語の *had better / it is better to* にあたる最も一般的かつ自然な表現。接続法節を取ることもできる（*Il vaut mieux que tu partes.*）。
  - □ **valoir** `/va.lwaʁ/` 【自/他】 価値がある；〜に値する (*Ça vaut la peine.*：それだけの価値がある)
- **1177 | au préalable** `/o pʁe.a.labl/` 【副句】 前もって，あらかじめ，事前に
  - (= **à l'avance**, **d'avance**)
  - ※ 【論理的で丁寧な副詞句】ある行動を起こす前の「前提手順」として事前に済ませておくことを表す。英語の *beforehand* に対応。

---

### No. 299 [♂ Remy & ♀ Vivienne]
> **« — Pardon d'interrompre ton repas, mais j'aimerais te parler en privé. — Je peux te recontacter tout à l'heure ? »**
> （— 食事中に邪魔してごめん、内密に話したいことがあるんだ。 — あとで連絡し直してもいい？）

- **1178 | le repas** `/ʁə.pa/` 【名・男】 食事，ご飯，一食
  - (= **le déjeuner**, **le dîner**; **le festin** [ごちそう])
  - ※ 【語末の s に注意】単数形でも語末に s があり不変（*un repas / des repas*）。フランス文化の誇り「フランスの美食術」は *le repas gastronomique des Français* としてユネスコ無形文化遺産に登録されている。
- **1179 | en privé** `/ɑ̃ pʁi.ve/` 【副句】 内密に，非公式に，人目を避けて；個人的に
  - (= **en tête-à-tête** [差し向かいで], **en secret**, **confidentiellement**)
  - ※ 英語の *in private*。公の場ではなく、他人に聞かれない場所で1対1で話す状況を表す。
  - (↔ en public 公の場で)
  - □ **privé(e)** `/pʁi.ve/` 【形】 私的な，私立の；個人の (*la vie privée*：私生活，プライバシー)
- **1180 | recontacter** `/ʁə.kɔ̃.tak.te/` 【他】 （人に）再び連絡を取る，折り返し連絡する
  - (= **rappeler** [折り返し電話する], **joindre de nouveau**)
  - ※ 【ビジネス・日常の最頻出語】英語の *get back to someone* にあたる便利な動詞。*« Je vous recontacte dès que possible. »*（できるだけ早く折り返しご連絡します）。
  - □ **le contact** `/kɔ̃.takt/` 【名・男】 接触，連絡先 (*garder le contact*：連絡を取り続ける)
- **1181 | tout à l'heure** `/tu.t‿a l‿œʁ/` 【副句】 ①のちほど，まもなく，あとで ②さっき，先ほど
  - (= **plus tard** [あとで] / **tout récemment** [さっき])
  - ※ 【時制によって意味が変わる超重要表現】未来の文脈では「あとで，のちほど（= in a little while）」、過去の文脈では「さっき，先刻（= a little while ago）」。別れの挨拶 *« À tout à l'heure ! »* は「またあとでね！」。

---

### No. 300 [♀ Denise]
> **« Le cuisinier a été stupéfait par son appétit incroyable. »**
> （料理人は、彼の信じられないほどの旺盛な食欲に目を見張った。）

- **1182 | le cuisinier / la cuisinière** `/kɥi.zi.nje, -ɛʁ/` 【名】 料理人，コック；【名・女】ガス台，調理器
  - (= **le chef**, **le cuistot** [（俗）料理番])
  - ※ 【多義の急所】女性名詞 *la cuisinière* は「女性の料理人」と「コンロ・調理台レンジ」の双方を指す。
  - □ **la cuisine** `/kɥi.zin/` 【名・女】 料理；台所
  - □ **cuisiner** `/kɥi.zi.ne/` 【他/自】 料理する；（比喩）厳しく尋問する
- **1183 | stupéfait(e)** `/sty.pe.fɛ, -t/` 【形】 仰天した，呆然とした，目を見張った
  - (= **ébahi(e)** [あっけにとられた], **sidéré(e)** [茫然自失の], **étonné(e)**)
  - ※ 【驚きの強度】単なる *étonné*（驚いた）を超えて、言葉を失うほど「あっけにとられて呆然とする」強い驚きを表す。
  - □ **la stupéfaction** `/sty.pe.fak.sjɔ̃/` 【名・女】 驚愕，呆然
- **1184 | l'appétit** `/a.pe.ti/` 【名・男】 食欲；（比喩）欲望，意欲
  - ※ 【食事の挨拶】食事前の定番の挨拶 *« Bon appétit ! »*（召し上がれ！）。ことわざ *« L'appétit vient en mangeant. »*（食欲は食べているうちに湧いてくる＝やり始めればやる気が出る）。語末の t は無音。
  - □ **appétissant(e)** `/a.pe.ti.sɑ̃, -t/` 【形】 食欲をそそる，おいしそうな
- **1185 | incroyable** `/ɛ̃.kʁwa.jabl/` 【形】 信じられない，並外れた，桁外れの
  - (= **invraisemblable** [ありそうもない], **prodigieux(-euse)** [驚異的な], **formidable**)
  - ※ 【語形成】*in-*（否定） + *croire*（信じる） + *-able*。信じがたい出来事のほか、口語で「ものすごい、素晴らしい」という感嘆表現（*C'est incroyable !*）としても超頻出。
  - (↔ croyable 信じられる)

---

### No. 301 [♂ Remy & ♀ Vivienne]
> **« — Que se passe-t-il là-bas ? Je suis curieux de savoir. — Je n'en ai pas la moindre idée ! »**
> （— あそこで何が起きているんだい？気になるな。 — さっぱり見当もつかないわ！）

- **1186 | se passer** `/sə pa.se/` 【代動】 （事件・事態が）起こる，生じる，展開する
  - (= **arriver**, **avoir lieu**, **se dérouler**)
  - ※ 【日常最頻出の疑問文】*« Qu'est-ce qui se passe ? »* / *« Que se passe-t-il ? »*（何が起きているの？／どうしたの？）。英語の *What's going on?* や *What happened?* に直結する。
- **1187 | curieux(-euse)** `/ky.ʁjø, -øz/` 【形】 ①知りたがっている，好奇心の強い ②奇妙な，不思議な
  - (= **désireux(-euse) de savoir** [知りたがる]; **étrange**, **bizarre** [奇妙な])
  - ※ 【位置による意味変化】名詞の**後**に置くと「好奇心の強い（*un enfant curieux*）」、名詞の**前**に置くと「奇妙な（*une curieuse histoire*）」。成句 **être curieux de (+ inf.)** で「〜を知りたがる，気にかける」。
  - □ **la curiosité** `/ky.ʁjɔ.zi.te/` 【名・女】 好奇心；観光名所
  - □ **curieusement** `/ky.ʁjøz.mɑ̃/` 【副】 奇妙なことに，好奇心を込めて
- **1188 | la moindre idée** `/mwãdʁ i.de/` 【名句】 （否定文で）少しの考え・見当，さっぱりわからないこと
  - (= **aucune idée** [見当もつかない])
  - ※ 【強い否定の定番】*moindre* は *petit* の優等比較・最上級。「少しの（least）」。**Je n'en ai pas la moindre idée.** は英語の *I have no idea.* / *I haven't the slightest idea.* に完全対応する最重要成句。
  - □ **moindre** `/mwɛ̃dʁ/` 【形】 より小さい，より少ない (◆ *le moindre / la moindre*: 最もわずかな)

---

### No. 302 [♂ Henri]
> **« Des admirateurs enthousiastes traînaient près de la sortie arrière, espérant apercevoir Michel. »**
> （興奮したファンたちが、ミシェルを一目見ようと裏口の周りにたむろしていた。）

- **1189 | un(e) admirateur(-trice)** `/ad.mi.ʁa.tœʁ, -tʁis/` 【名】 ファン，崇拝者，称賛者
  - (= **le fan**, **l'adepte**)
  - ※ 【格調高い語彙】英語からの外来語 *le/la fan* よりも品格があり、フランス語の正統な「熱心なファン・愛好者」を指す。
  - □ **admirer** `/ad.mi.ʁe/` 【他】 称賛する，感嘆する，見惚れる
  - □ **l'admiration** `/ad.mi.ʁa.sjɔ̃/` 【名・女】 称賛，感嘆
- **1190 | enthousiaste** `/ɑ̃.tu.zjast/` 【形】 熱狂的な，熱心な，意気揚々とした；【名】熱狂的な愛好者
  - (= **passionné(e)** [情熱的な], **surexcité(e)** [興奮した], **fervent(e)**)
  - ※ 【多義と感情】ギリシャ語「神が宿った」に由来。イベント・計画・アイドルに心を躍らせて夢中になっている様子を描く。
  - □ **l'enthousiasme** `/ɑ̃.tu.zjazm/` 【名・男】 熱狂，情熱，意気込み
- **1191 | traîner** `/tʁɛ.ne/` 【自】 たむろする，ぶらつく；だらだら過ごす；【他】 引きずる
  - (= **flâner** [ぶらつく], **rôder** [うろつく], **errer**)
  - ※ 【若者・街頭の生きた表現】目的もなく出口付近や街角で「たむろする・時間をつぶす（= hang around）」。物を「片付けずに放り出しておく」意味もある（*Tes affaires traînent partout.*）。
- **1192 | apercevoir** `/a.pɛʁ.sə.vwaʁ/` 【他】 （遠く・一瞬のものを）ちらりと目にする，見かける；気づく
  - (= **entrevoir** [ちらりと見る], **distinguer** [見分ける], **remarquer**)
  - ※ 【英語 catch a glimpse of... に直結】意識してじっと見る（*regarder*）のではなく、動く人影などが「一瞬視界に入って捉える」ことを表す。代名動詞 *s'apercevoir de qc* は「〜に気づく」。
  - □ **un aperçu** `/a.pɛʁ.sy/` 【名・男】 概要，一瞥，プレビュー

---

### No. 303 [♀ Denise]
> **« En se trouvant face à cette vedette, ils lui ont réclamé un autographe. »**
> （その大スターと対面すると、彼らはサイン（自筆署名）を求めた。）

- **1193 | face à** `/fas a/` 【前置詞句】 〜に直面して，〜と対面して，〜を前にして
  - (= **devant** [〜の前で], **vis-à-vis de** [〜に対して])
  - ※ 【身体・状況の対面】物理的に人と「面と向かい合う」こと、また「危機に直面する（*face à la crise*）」ことの双方で多用される。
  - □ **la face** `/fas/` 【名・女】 （物の）面，表面；顔 (*en face de*：〜の向かいに)
- **1194 | la vedette** `/və.dɛt/` 【名・女】 スター，花形，有名人，主役
  - (= **la star**, **la célébrité**, **la personnalité**)
  - ※ 【フランス文化の象徴的呼称】映画・演劇・音楽界の「大スター」。冠詞は常に女性名詞（男性スターであっても *cette vedette*）。
  - □ **être en vedette** `/ɛtʁ ɑ̃ və.dɛt/` 【成句】 （看板・ポスターで）トップに名前が出る，注目を浴びる
- **1195 | réclamer** `/ʁe.kla.me/` 【他】 （強く・当然の権利として）要求する，ねだる，求める
  - (= **exiger** [要求する], **demander avec insistance**, **revendiquer**)
  - ※ 【要求の強さ】単なる *demander* よりも積極的・熱烈に「ちょうだいとねだる／要求する」ニュアンスを含む。
  - □ **la réclamation** `/ʁe.kla.ma.sjɔ̃/` 【名・女】 苦情，クレーム，抗議 (*le service des réclamations*：お客様相談室)
- **1196 | un autographe** `/o.tɔ.ɡʁaf/` 【名・男】 （有名人の）サイン，自筆署名，直筆原稿
  - (= **la signature d'une célébrité**)
  - ※ 【使い分けの急所】契約書や公的書類に本人が行う通常の署名は **la signature**。芸能人・スポーツ選手・著名人がファンに書く記念の「サイン」は必ず **un autographe** と言う（英語の *autograph* と *signature* の関係と同じ）。
"""

fpath = os.path.join(SECTIONS_DIR, 'section_26.md')
with open(fpath, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Successfully wrote {fpath}")
