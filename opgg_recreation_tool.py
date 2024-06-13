import imgkit

game_type = "Arena"
champion_name = 'Aatrox'
level = 15
win = False
duration = '20m 23s'
result = 'Defeat' if win == False else 'Victory'
timing = '10 minutes ago'
kills = 5
deaths = 4 
assists = 3
kda = 0.14
game_color = 'red' if win == False else 'blue'
background_color = ' pink' if win == False else 'lightblue'
champion_image = f"https://ddragon.leagueoflegends.com/cdn/14.11.1/img/champion/{champion_name}.png"
body = f"""
<!DOCTYPE html>
    <html>
    <head>
        <meta content="jpg"/>
        <meta  content="Landscape"/>
    </head>
    <body>
        <div class='container' style='display: flex; height: 100%; flex-direction: column; width: 100%; background-color: {background_color}; border-radius: 1px; overlow: hidden;'>
            <div class='deco' style='position: absolute; display: block; height: 84%; width: 6px; min-width: 6px; border-radius: 1px; background-color: {game_color};'></div> 
            <div class='inner' style='display: flex; flex-direction: column; min-width: 100%; width: 100%; gap: 8px; padding: 0px 12px; unicode-bidi: isolate'>
                <div class='left-section' style='margin-top: 3px; float: left; width: 108px; display: flex; flex-direction: column; gap: 8px; font-size: 12px; font-weight: 400; line-height: 16px; color: gray;'>
                        <div class='head-group' style='display: flex; flex-direction: column; white-space: nowrap; font-size: 12px; font-weight: 400; line-height: 16px; color: gray'>
                            <div class='game-type' style='font-weight: 700; display: block; white-space: nowrap; font-size: 12px; line-height: 16px; color: red'>{game_type}</div>
                            <div class='timestamp' style='display: block;font-size: 12px; font-weight: 400; line-height: 16px; color: gray; white-space: nowrap'>
                                <div style='position: relative;'>{timing}</div>
                            </div>
                        </div>
                        <div class='divider' style='margin-top: 5px; margin-bottom: 5px; width: 48px; height: 1px; background-color: red; opacity: 0.2; font-size: 12px; font-weight: 400; line-height: 16px; color: gray'></div>
                        <div class='head-group' style='display: flex; flex-direction: column; white-space: nowrap; font-size: 12px; font-weight: 400; line-height: 16px; color: gray'>
                            <div class='result' style='font-weight: 700; display: block; white-space: nowrap; line-height: 16px; color: red'>{result}</div>
                            <div class='length' style='display: block; white-space: nowrap; font-size: 12px; font-weight: 400; line-height: 16px; color: gray;'>{duration}</div>
                        </div>
                    </div> 
                </div>   
                <div class='middle-section' style='margin-top: 5px; margin-left: -20px; display: flex; flex-direction: column; float: left; -webkit-box-pack: start; justify-content: flex-start; height: 87%; gap: 2px; flex: 1 1 0%; font-size: 12px; max-height: 100%'>
                    <div class='main' style='display: flex; align-items: center; gap: 12px; display: flex; -webkit-box-align: center; align-items: center; gap: 4px; height: 58px; font-size: 12px;'>
                       <div class='info' style='display: flex; float: left; -webkit-box-align: center; align-items: center; gap: 4px; height: 58px; font-size: 12px; max-height:100px'>
                                        <div class='champion' style='position: relative; display: flex; -webkit-box-pack: center; justify-content: right; -webkit-box-align: center; align-items: right; min-width: 48px; '>
                                            <img src={champion_image} width='48' height='48' style='border-radius: 50%; border: 0; vertical-align: middle; max-width: 100%; width: 48px; aspect-ratio: auto 48 / 48; height: 48px; '>
                                            <span class='champion-level' style='position: absolute; left: 30px; bottom: 0px; display: inline-block; width: 20px; height: 20px; font-size: 11px; font-weight: 400; line-height: 14px; color: rgb(255, 255, 255); background: rgb(32, 45, 55); border-radius: 50%; text-align: center; line-height:18px'>{level}</span>
                                        </div>
                                        <div class='GameLoadout' style='position: absolute; left: 170px; bottom: 40px; display: flex; gap: 2px; font-size: 12px;'>
                                            <div class='loadout-group' style='display: flex; float:left; flex-direction: column; gap: 2px; font-size: 12px;'>
                                                <div class='spell' style='position: relative; display: flex; overflow: hidden; border-radius: 4px;'>
                                                    <img src='https://ddragon.leagueoflegends.com/cdn/14.12.1/img/spell/SummonerFlash.png' width='22' height='22' alt='Flash' style='border-radius: 4px;'>
                                                </div>
                                                <div class='spell' style='position: relative; display: flex; overflow: hidden; border-radius: 4px;'>
                                                    <img src='https://ddragon.leagueoflegends.com/cdn/14.12.1/img/spell/SummonerHeal.png' width='22' height='22' alt='Heal' style='border-radius: 4px;'>
                                                </div>
                                            </div>
                                            <div class='loadout-group' style='display: flex; float:right; flex-direction: column; gap: 2px; font-size: 12px;'>
                                                <div class='rune rune-primary' style='position: relative; display: flex; overflow: hidden; border-radius: 50%; font-size: 12px;'>
                                                    <img src='https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/Domination/Electrocute/Electrocute.png' width='22' height='22' style='background: rgb(0, 0, 0); aspect-ratio: 1 / 1; min-width: 22px; border: 0; vertical-align: middle; max-width: 100%;width: 22px; height: 22px; overflow-clip-margin: content-box; overflow: clip; border-radius: 50%;'>
                                                </div>
                                                <div class='rune rune-secondary' style='position: relative; display: flex; overflow: hidden; border-radius: 50%; font-size: 12px;'>
                                                    <img src='https://ddragon.leagueoflegends.com/cdn/img/perk-images/Styles/7202_Sorcery.png' width='22' height='22' style='background: rgb(0, 0, 0); aspect-ratio: 1 / 1; min-width: 22px; border: 0; vertical-align: middle; max-width: 100%;width: 22px; height: 22px; overflow-clip-margin: content-box; overflow: clip; border-radius: 50%;'>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                    <div class='kda-stats' style='width: 108px; position: absolute; margin-top: 5px; margin-left: 120px; display: flex; flex-direction: column; align-items: flex-start; gap: 2px; font-size: 12px;'>
                                        <div class='kda' style='color: gray; font-size: 15px; font-weight: 700; line-height: 22px; display: block;'>
                                            <span style='color: black; font-size: 15px; font-weight: 700; line-height: 22px;'>{kills}</span> / <span class='d' style='color: red; font-size: 15px; font-weight: 700; line-height: 22px;'>{deaths}</span> / <span style='color: black; font-size: 15px; font-weight: 700; line-height: 22px;'>{assists}</span>
                                        </div>
                                            <div class='kda-ratio' style='color: var(--gray500); font-size: 12px; font-weight: 400; line-height: 16px; display: block;'>{kda}:1 KDA</div>
                                        </div>
                                    
                    <div class='game-stats' style='position: absolute; margin-top: 5px; margin-left: 200px; display: flex; flex-direction: column; height: 58px; flex: 1 1 0%; padding-left: 8px; border-left-width: 1px; border-left-style: solid; border-color: red; color: gray; font-size: 11px; font-weight: 400; line-height: 14px;'>
                                        <div class='p-kill' style='color: red'>
                                            <div style='position: relative;'>P/Kill 40%</div>
                                        </div>
                                        <div class='ward'>Control Ward 1</div>
                                        <div class='cs'>
                                            <div style='position: relative;'>CS 13 (0.9)</div>
                                        </div>
                                        <div class='avg-tier'>
                                            <div style='position: relative;'>diamond 3</div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            </div>

    </body>
    </html>"""

options = {'height': 100, 'width': 540, 'disable-smart-width': ''}
imgkit.from_string(body, 'out.jpg', options=options)

#imgkit.from_file('test.html', 'out.jpg')
#print(str(type(v)) == "<class 'bytes'>")
#imgkit.from_url("https://www.op.gg/summoners/na/Almourex-NA1", 'out.jpg')

