"""Curated observations from chronological reference sheets, not source code recovery."""
import json
from pathlib import Path
P=Path(__file__).parent
rows=[
(0,4,'night_office_title','Navy office with rows of seated workers; skyline window grid; hanging EXIT sign. Large cream Bengali headline upper-left, final word vermilion.','seated workers, desks, monitors, skyline, hanging sign','headline reveal; fine grain; small window lights'),
(4,10,'night_office_offer','Same navy office without giant title. Cream mono offer strip above workers; envelopes appear near desks.','seated workers, envelopes, title strip','envelopes pop in; static repeated desk grid'),
(10,17,'office_headcount_card','Cream card overlays office. Ten-by-ten worker grid, red top portion, large red percentage and explanatory Bengali type.','worker pictograms, card, red edge','icon recoloring and counter reveal'),
(17,28,'layoff_walkers_counter','Cream city silhouette, horizontal ground line. Walking workers carry boxes below a large black number chip at upper-left.','walkers, boxes, skyline, number chip','counter increments; walkers pass and fade'),
(28,35,'layoff_year_comparison','Two rectangular grids of different heights at right, with workers and year captions; large black number chip remains left.','two grid towers, people, dashed measurement bracket','bars grow; comparison bracket draws'),
(35,41,'street_shield','Dhaka street with vermilion-shirt guide raising phone; tea stall, seated customer, palm, wires, mosque silhouette and walkers. Large checked shield above guide.','guide, phone, shield, tea stall, skyline','guide arm raises; shield cracks/disappears; walkers cross'),
(41,54,'profession_rooms','Three outlined rooms: doctor and bed, teacher and green board/classroom desks, garment worker and sewing machine. Camera travels horizontally through rooms.','doctor, bed, teacher, board, garment worker, sewing table','camera pan; checklist shields over professions'),
(54,70,'ai_lab_survey','Navy inset AI lab within cream page, three grey desk workers with blue screens and blue orb. Survey clipboard appears to its upper-right.','lab, blue orb, three seated workers, survey clipboard','orb pulses; clipboard enters'),
(70,84,'survey_slider_crowd','Lab at left, mixed crowd at right; horizontal 0–100% ruler above with red question-mark handle.','mixed crowd, lab, slider, labels','slider moves; percentages reveal'),
(84,86,'green_halftone_transition','Green slab fills frame; edge uses cream/green halftone dots.','halftone sweep','wipe'),
(86,94,'phone_chat','Seated person holding phone in cream room with barred window. Oversized smartphone chat UI at right.','seated person, chair, smartphone, window','chat lines reveal; red underline'),
(94,105,'garage_engine_analogy','Grey garage with blue engine on brown workbench, wall tools, stacked tires, mechanic and guide. Road continues to the right with distant destination sign.','guide, mechanic, engine, workbench, tires, wall tools, road','camera pans to road; car assembly analogy'),
(105,118,'agent_workflow','Grey woman at left, blue orb center; filing cabinet above-left and computer below-right connected by blue dashed paths.','woman, orb, cabinet, computer, dashed links','nodes appear sequentially; link flow'),
(118,124,'four_shopfronts','Four dark buildings on cream skyline, blue window grids, Bengali signs for hospital, bank, legal advice and call center.','four shopfronts, blue windows, city','windows illuminate; buildings enter'),
(124,130,'curtain_reveal','Vermilion guide stands before tall grey vertical panels/curtains with halftone lower area.','guide, curtain panels','panels sweep/reveal'),
(130,134,'world_map_transition','Pale world map with dark North America; green halftone sweep crosses frame.','world map, halftone','wipe'),
(134,144,'relaxed_desk','Cream room, barred window upper-right, reclining grey figure with legs on table and small laptop. Red-edged opinion card upper-left.','reclining person, chair, table, laptop','subtle pose changes; card reveal'),
(144,151,'job_is_bundle','Guide points to a large outlined square with Bengali word for job. Right edge dissolves to halftone. Blue robot arm opposite.','guide, job card, robot arm','card breaks into task tiles'),
(151,157,'task_tiles','Two rows of four outlined task tiles above guide: email, meeting, report, calls, sheets, decide, teach, plan. Robot arm at right.','guide, task tiles, robot arm','tiles appear; arm pivots'),
(157,167,'ten_doctors_timebars','Row of ten doctors along a baseline. Stacked time bars above, tiny paperwork icons beside them.','ten doctors, time bars, paperwork','bars reveal and fill'),
(167,174,'doctor_headcount_reduction','Blue orb removes upper paperwork segments from time bars; six dark bars/people retained, four become outlined/faded.','doctors, bars, orb','bar segments peel away; four fade'),
(174,180,'hospital_remaining_work','Three patient beds with doctors attending; floating blue screen above.','doctors, beds, patient markers, blue screen','person gestures; screen text lines'),
(180,191,'desk_grid_eighty_percent','Ten-by-ten grid of tiny desks/workers; blue screens progressively fill most cells; small red guide icon anchors grid.','desk pictograms, screens, blue percentage','cell-by-cell blue fill'),
(191,196,'grid_zoom_task_detail','Camera zoom into one cream grid cell showing simplified person and large blue monitor.','person pictogram, desk, blue monitor','hard zoom/push-in'),
(196,203,'rice_manual_labor','Green rice field with repeated bent workers cutting rice, huts, palms, dark green trees and a large red sun.','field workers, rice, huts, palms, sun','bending work cycle; field texture'),
(203,209,'combine_harvester','Small combine harvester crosses the same field; standing workers reduce.','harvester, driver, rice, workers','machine translates; wheel rotates; labor changes'),
(209,219,'agriculture_labor_card','Cream evidence card above field: worker pictograms and red -70% callout; few workers retained.','field, labor card, worker icons','card slides in; icons fade'),
(219,227,'agriculture_ten_to_three','Large 10-to-3 Bengali count above field; fading row of seven workers, three retained near sacks.','workers, sacks, count arrow','ghost silhouettes fade; check mark draws'),
(227,233,'office_row_transition','Rice scene gives way to cream office with row of seated workers and broad skyline window.','office desks, workers, window','horizontal scene transition'),
(233,240,'night_creator_desk','Navy room, lone grey person at desk, blue halftone glow above laptop; city window at upper-right.','creator, desk, laptop, window, glow','glow pulses; small page icons emerge'),
(240,245,'code_window','Floating cream code editor with blue title bar over night desk.','code window, creator desk','code line reveal; cards orbit'),
(245,255,'editing_time_comparison','Two adjacent night desk panels, clocks above, script/video effort bars at right.','editing monitors, clocks, effort bars','camera slide; red script bar vs short blue video bar'),
(255,268,'empty_editor_chair','Spotlight cone over desk and chair in navy room. Person leaves; empty workstation remains.','spotlight, desk, chair, departing person','figure fades/walks out; light holds'),
(268,278,'jobs_at_tea_stall','Two people converse beside tea stall; one holds AI-jobs chart card.','two people, tea stall, chart card','arm raises; card tilts'),
(278,292,'headcount_ledger','Large ruled two-column table with red header. Left has 100 worker icons, right blue AI jobs; left reduces to 50 while right grows to 15.','ledger, human icons, blue icons, Bengali labels','icons fade/fill; counts update'),
(292,297,'newspaper_fivefold','Skewed outlined newspaper panel with giant Bengali headline; blue final 5-times phrase. Small celebratory person below.','newspaper, person','panel pops in; raised arms'),
(297,305,'total_headcount_compare','Two worker grids labeled before and now, including blue AI roles: 103 vs 65; red current total.','two headcount grids, before/after labels','grids appear; total reveal'),
(305,308,'blue_chapter_wipe','Electric blue vertical slabs and narrow red separator pass across cream scene.','blue slabs','horizontal wipe'),
(308,318,'teacher_scale','Teacher at green board left, tiny learner grid at right expands dramatically.','teacher, board, learner grid','headcount grid expands; teacher holds blue device'),
(318,333,'garment_factory','Four seated sewing workers under ceiling fans. Inset panel shows blue robot arms and three-of-four blocks; numbered issue cards appear.','sewing workers, machines, fans, robot arms, issue cards','sewing gestures; fan rotation; panel reveal'),
(333,341,'robot_cost_comparison','Robot arm at left next to tall cost stack and many dollar symbols; human worker at right with short stack.','robot arm, worker, cost stacks','cost bars rise'),
(341,345,'robot_economics_grid','Large thousand-cell pale grid with only a few blue cells and large blue 0.3% callout.','dense grid, three blue cells, percentage','tiny cells highlight'),
(345,352,'robot_soft_cloth','Blue robot arm near table of fabric; cloth droops/falls, grey woman gestures.','robot arm, fabric, table, woman','joint motion; cloth falls'),
(352,357,'garment_temporary_safety','Two sewing workers below large green check and black hourglass.','workers, check, hourglass, fans','check draws; hourglass appears'),
(357,365,'robot_imitation_learning','Garment work scene with pale blue training enclosure where robot mirrors a person; calendar/ability grid above.','workers, imitation-learning enclosure, grid','robot follows pose; cells fill'),
(365,374,'digital_work_panels','Cream frame divides into four scenes: office paperwork, bank teller, shared desks, freelancer under fan.','four panels, workers, desks, bank booth','camera zoom out to four-panel layout'),
(374,382,'copyable_ai','Blue orb in center of four-panel layout with many small blue nodes; screens turn blue.','orb, copies, panels','particles radiate; blue screens illuminate'),
(382,390,'small_cheap_ai','Zoom back into office panel: small blue orb handles file stacks, red check under monitor.','worker, monitor, small orb, files','small orb moves between work items'),
(390,404,'government_paperwork','Cream government office with cabinet left, seated official center, piles of tied files and standing clerk; ceiling fans and clock. Blue halftone outline highlights entire desk.','official, clerk, tied files, cabinet, fans, clock','files accumulate; blue frame sweeps over desk'),
(404,411,'recruitment_reduction','Notice board of recruitment lines with red strike-through marks at left; empty desk and no-new-hire sign at right.','notice board, desk, two applicants','notice lines strike through'),
(411,424,'government_exam_queue','Long mixed queue to examination-center building. Large black number cards count applicants and positions.','queue, examination building, counters','counter rolls; queue advances'),
(424,432,'chairs_and_queue','Three red outline chairs along baseline; surrounding crowd/queue emphasizes competition.','red chairs, applicants','chairs reduce; crowd accumulates'),
(432,437,'counterargument_intro','Grey figure gestures in large cream negative space; red numbered circle introduces next section.','presenter, red counter badge','badge drops; gesture'),
(437,449,'accounting_history','Cream office with spreadsheet monitor, filing papers and comparison card: crossed-out clerks versus growing accountant icons.','accountants, desk, spreadsheet, icon comparison','icons cross out/fill; workers pass'),
(449,456,'healthcare_queue','Long line outside local health complex with red medical cross and green sign.','mixed queue, clinic','queue movement'),
(456,462,'healthcare_density','Pictogram grid with green icons for Bangladesh and comparative density labeling.','medical icons, density grid','grid fills'),
(462,472,'village_health_network','Mother with child and blue phone among four huts and palms; blue orb above connects dashed arcs to village windows.','mother, child, huts, palms, orb','arcs draw and pulses travel'),
(472,482,'unlimited_demand_funnel','Blue AI pipe pours through open funnel toward growing line of people; healthcare/education icons label funnel.','pipe, funnel, people, medical/education icons','blue flow, expanding crowd'),
(482,489,'saturated_office_demand','Companion pipe pours into a bounded office rectangle packed with tiny worker rows; overflow dislodges icons as few people remain outside.','pipe, full office block, displaced people','fill rises; worker tiles move out'),
(489,501,'jobs_data_chart','Large outlined chart with near-flat black line, handheld magnifier, two observers; red section-two badge.','chart, magnifier, two people','magnifier moves over line'),
(501,507,'ai_washing_podium','Speaker behind podium and AI-labeled large box, audience applauds; tiny blue AI-WASHING tag.','podium, box, speaker, audience','box reveals; arms lift'),
(507,513,'rank_five_chart','Dark panel containing five grey horizontal bars; fifth bar partly blue and labeled AI, red-shirt guide at right.','ranked bar chart, guide','bars reveal; fifth highlights'),
(513,520,'hidden_hiring_below_surface','Cream upper strip with tipped chair; navy lower region and halftone texture, spotlight on dashed empty chairs under hiring label.','surface line, empty chairs, spotlight','vertical reveal into lower region'),
(520,526,'editor_never_hired','Empty editor workstation with two dark screens and vacancy sign; standing grey figure gestures.','empty chair, monitors, figure, sign','arm gesture; chair remains empty'),
(526,533,'late_data_wave','Guide seated holding rising-chart card; thick blue wave rises along bottom edge.','guide, chart, chair, blue water','wave oscillates and rises'),
(533,543,'atm_human_queue','Blue-screen ATM at left, human teller booth at right with guide serving; queue prefers human; clipboard survey overhead.','ATM, teller booth, queue, survey clipboard','queue forms; checkbox ticks'),
(543,548,'human_cost_tenfold','Human teller and tall cost stack with red 10x left; ATM and tiny cost stack right.','teller, ATM, cost stacks','cost reveal'),
(548,556,'mobile_money_doubt','Two people with phones; thought bubble shows phone and money under dark halftone vignette.','two people, phones, money thought bubble','bubble grows; dotted halo'),
(556,563,'mobile_money_shop','Green signed mobile banking shop connected by dashed arc to village home; person raises phone.','shop, home, phone, dashed arc','arc draws; green check'),
(563,567,'chapter_seven_card','Electric blue page, cream Bengali heading left with black block behind lower line; enormous striped cream 07 on vermilion disc right.','chapter numeral, red disc, stripes','sliding chapter typography'),
(567,580,'task_conveyor','Conveyor carries outlined hand/brain task boxes through tall blue AI machine; outputs turn blue.','conveyor, task boxes, AI machine','belt and boxes translate; machine glows'),
(580,587,'relaxed_hammock','Guide lies in hammock between two palms across cream scene.','guide, hammock, palms','gentle hammock sway'),
(587,594,'self_audit_laptop','Guide seated at laptop; task tiles array overhead.','guide, laptop, task tiles','tiles reveal and descend'),
(594,603,'ai_human_task_blocks','Blue task blocks pile beside laptop; outlined red-edged human task blocks remain on dark pedestal at right.','guide, task blocks, two platforms','tiles sort into piles'),
(603,610,'repeat_audit_calendar','Same desk/task piles with four small red calendar/check icons upper-right; one human task shifts to blue pile.','task piles, calendars','calendar ticks; tile transfers'),
(610,621,'street_comment_box','Return to detailed Dhaka street, guide using phone. Large cream red-shadow comment form floats above center.','street, guide, phone, comment card, tea stall','comment types; pedestrians/rickshaw move'),
(621,629,'street_tech_friend','Guide and grey friend meet, phone/chat bubble between them; same Dhaka street.','guide, friend, conversation bubble, street','gesture/handshake; bubble changes'),
(629,637.166667,'dark_sources_endcard','Navy final card with cream/red Bengali headline upper-left and two small mono source columns below. Halftone navy texture bottom-left.','headline, source columns, halftone','settle and hold')]
scenes=[]
for i,(a,b,name,layout,props,motion) in enumerate(rows):
    scenes.append({'id':f'ref_{i+1:03d}','start_approx':a,'end_approx':b,'scene':name,'layout':layout,'props':[v.strip() for v in props.split(',')],'observed_or_inferred_motion':motion,'evidence':{'overview_every_6s':'reference/video2/contact_sheets/','time_precision':'Approximate editorial boundary; validate with every-frame atlas and decoded PTS before exact matching.'}})
(P/'scene_catalog.json').write_text(json.dumps({'provenance':'Curated visual observations from all nine original 6-second overview sheets; supplemented by the new 2-second overview review. This is an observational reconstruction, not recovered original source code.','scenes':scenes},ensure_ascii=False,indent=2))
(P/'SCENE_TIMELINE.md').write_text('# Reference scene timeline\n\nThese are visual observations, not fact-checks of the narrated claims. Boundaries are approximate; use `frames.csv`, `index.html`, and source video for frame-accurate cuts. The original images and their timestamps take priority over the supplied prose summary.\n\n| Approx. seconds | Scene | Composition and props | Motion evidence/inference |\n|---|---|---|---|\n'+''.join(f'| {a:g}–{b:g} | `{n}` | {l} | {m} |\n' for a,b,n,l,p,m in rows))
print(len(scenes))
# Correct the older montage's approximate labels against the fresh decoded-PTS
# overview (one thumbnail every 2s) and detected transition windows.
starts={
'night_office_title':0,'night_office_offer':5,'office_headcount_card':13,
'layoff_walkers_counter':17.733333,'layoff_year_comparison':28.8,'street_shield':36.5,
'profession_rooms':43.4,'ai_lab_survey':56.1,'survey_slider_crowd':70,
'green_halftone_transition':81.066667,'phone_chat':86.866667,'garage_engine_analogy':96.666667,
'agent_workflow':110,'four_shopfronts':119.3,'curtain_reveal':126.766667,
'world_map_transition':134.433333,'relaxed_desk':137.133333,'job_is_bundle':147,
 'task_tiles':153,'ten_doctors_timebars':159,'doctor_headcount_reduction':168,
 'hospital_remaining_work':175,'desk_grid_eighty_percent':181.266667,
 'grid_zoom_task_detail':194.233333,'rice_manual_labor':197.4,'combine_harvester':203,
 'agriculture_labor_card':209,'agriculture_ten_to_three':219.7,'office_row_transition':230.333333,
 'night_creator_desk':233.6,'code_window':241,'editing_time_comparison':245,
 'empty_editor_chair':259,'jobs_at_tea_stall':272.333333,'headcount_ledger':281,
 'newspaper_fivefold':293.3,'total_headcount_compare':299,'blue_chapter_wipe':308.5,
 'teacher_scale':311,'garment_factory':320.666667,'robot_cost_comparison':335,
 'robot_economics_grid':340,'robot_soft_cloth':345,'garment_temporary_safety':354,
 'robot_imitation_learning':359,'digital_work_panels':369,'copyable_ai':377,
 'small_cheap_ai':384.266667,'government_paperwork':392.433333,
 'recruitment_reduction':406.866667,'government_exam_queue':413.533333,
 'chairs_and_queue':425,'counterargument_intro':435.4,'accounting_history':438,
 'healthcare_queue':452.233333,'healthcare_density':455,'village_health_network':465,
 'unlimited_demand_funnel':472.1,'saturated_office_demand':478,'jobs_data_chart':493,
 'ai_washing_podium':503,'rank_five_chart':508.5,'hidden_hiring_below_surface':513.533333,
 'editor_never_hired':522.8,'late_data_wave':529,'atm_human_queue':535.966667,
 'human_cost_tenfold':547,'mobile_money_doubt':551,'mobile_money_shop':557,
 'chapter_seven_card':565.966667,'task_conveyor':573,'relaxed_hammock':583.5,
 'self_audit_laptop':591,'ai_human_task_blocks':594,'repeat_audit_calendar':601,
 'street_comment_box':613.533333,'street_tech_friend':621.5,'dark_sources_endcard':631.2}
for s in scenes:
    s['start_approx']=starts[s['scene']]
    s['evidence']={'overview':'reference/analysis/overview/','full_frame_atlas':'reference/analysis/index.html','time_precision':'Scene boundary estimates from decoded PTS every two seconds and image-difference transition windows; semantic changes between sampled times may differ by up to about two seconds. Not original project timeline.'}
    if s['scene']=='green_halftone_transition':
        s.update(scene='survey_percentage_compare',layout='Two tall outline percentage bars on cream, workers beside each; blue fills reveal 75% vs 28%.',props=['two bars','survey participants','percentages'],observed_or_inferred_motion='bars fill to different levels; labels reveal')
    if s['scene']=='blue_chapter_wipe':
        s.update(scene='chapter_five_card',layout='Blue chapter page, cream Bengali heading left, striped cream 05 over red disc right; red/blue slabs transition in and out.',props=['chapter typography','red disc','striped numeral'],observed_or_inferred_motion='horizontal slab wipe and title reveal')
new=[
(40.966667,'chapter_two_card','Blue chapter page: cream Bengali heading at left, enormous striped 02 over vermilion disc at right.','chapter typography, striped numeral, red disc','blue/red slab wipe'),
(108.133333,'ai_factory_assembly','Two blue robot arms and seated operators on assembly-line car platform immediately after garage analogy.','robot arms, car platform, workers','conveyor movement and arm pivots'),
(131.3,'behind_the_scenes_scaffolding','Large electric-blue AI wall/screen concealed behind wooden scaffold, workers constructing it with guide at lower-left.','scaffolding, blue AI screen, workers, guide','reveal from curtains; construction poses'),
(144.266667,'chapter_three_card','Blue chapter page: job-is-a-bundle heading left; enormous striped 03 over red disc right.','chapter typography, striped numeral, red disc','slab wipe and settle'),
(432.3,'chapter_six_card','Blue chapter page: other-side heading left; enormous striped 06 over red disc right.','chapter typography, striped numeral, red disc','slab wipe'),
(561.233333,'preference_speed_bump','Green auto-rickshaw crosses small road speed bump with Bengali preference label; city silhouette behind.','auto-rickshaw, road, speed bump, skyline','vehicle slows over bump then continues'),
(569,'excuse_shield_calendar','Guide holds shield labeled excuse while red-topped calendar pages fall around him.','guide, shield, calendar pages','pages fall/rotate; shield cracks'),
(579.5,'if_to_when_stamp','Large black Bengali if is struck through in red; tilted red stamp says when.','large Bengali word, red strike, stamp','strike draws then stamp impacts')]
for start,name,layout,props,motion in new:
    scenes.append({'start_approx':start,'scene':name,'layout':layout,'props':props.split(', '),'observed_or_inferred_motion':motion,'evidence':{'overview':'reference/analysis/overview/','time_precision':'Approximate boundary from decoded-PTS overview and transition windows.'}})
scenes.sort(key=lambda s:s['start_approx'])
for i,s in enumerate(scenes):
    s['id']=f'ref_{i+1:03d}';s['end_approx']=scenes[i+1]['start_approx'] if i+1<len(scenes) else 19115/30
    s['start']=s['start_approx'];s['end']=s['end_approx']
    s['reference_frame']=round(((s['start']+s['end'])/2)*30)
meta={'provenance':'Curated visual observations from all 11 newly decoded two-second overview sheets covering 0–636s. All 19,115 frames are computationally fingerprinted and indexed. This is an observational reconstruction, not recovered original source code.','timing_warning':'Old reference/video2/contact_sheets labels are offset from actual source presentation times. Use the new reference/analysis/overview and frames.csv as authoritative timing evidence. Scene boundaries are approximate editorial estimates; start/end aliases are provided for reconstruction, not a claim of exact original cuts.','scenes':scenes}
(P/'scene_catalog.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2))
(P/'SCENE_TIMELINE.md').write_text('# Reference scene timeline\n\n'+meta['provenance']+'\n\n'+meta['timing_warning']+'\n\nThese observations describe images; they do not independently verify the narrated factual claims.\n\n| Approx. seconds | Scene | Composition | Motion evidence/inference |\n|---|---|---|---|\n'+''.join(f"| {s['start']:.3f}–{s['end']:.3f} | `{s['scene']}` | {s['layout']} | {s['observed_or_inferred_motion']} |\n" for s in scenes))
print('Corrected scenes:',len(scenes))
