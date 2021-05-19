from friends import *
from manimlib import AnimationGroup as AG

FADE_BUFF = MED_LARGE_BUFF
YELLOW_F = "#F7F642"
BOX_C = YELLOW_F
SEC_C = YELLOW_F
GRAD_A = (YELLOW_B, PINK)

def src(item):
    return "invariants/assets/" + item

def gen_f12():
    return Tex("f12", tex_to_color_map={"12":YELLOW_F}, font_size=160)

class MathCompetitions(Scene):
    """
    Scene describing context of AMC/math competitions
    """
    def construct(self):
        math_comps = Text("Math Competitions")
        math_comps_ul = Underline(math_comps)
        title = VGroup(math_comps, math_comps_ul)
        
        self.play(
            AG(
                Write(math_comps, run_time=1.5),
                GrowFromEdge(math_comps_ul, LEFT, rate_func=smooth, run_time=1),
                lag_ratio=0.4
            )
        )

        conf_amc = {"font_size":55}
        maa_color = "#3256A4"

        maa_logo = ImageMobject("invariants/assets/maa_bg.png", height=2)
        american = Text("American", **conf_amc)
        math = Text("Math", **conf_amc)
        competition = Text("Competition", **conf_amc)

        amc = Group(maa_logo, american, math, competition)
        for obj in amc: obj.next_to(ORIGIN)
        amc.arrange(DOWN, aligned_edge=LEFT, buff=MED_LARGE_BUFF)
        amc.shift(DOWN * MED_SMALL_BUFF)

        VGroup(american[0], math[0], competition[0]).set_color(maa_color)

        self.play(
            AG(
                title.animate.to_edge(UP),
                #Write(amc),
                #*(FadeIn(m, UP) for m in amc),
                AG( *(FadeIn(m, UP*FADE_BUFF) for m in amc), lag_ratio=0.1 ),
                lag_ratio=0.4
            )
        )

        cen_buff = 3

        conf_facts = { "font_size":40, "t2c": { "75": maa_color, "25": maa_color } }
        facts = VGroup(Text("‣ 75 minutes", **conf_facts), Text("‣ 25 problems", **conf_facts))
        facts.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        facts.shift(RIGHT * cen_buff)

        self.play(
            AG(
                AG(
                    *(m.animate.shift(LEFT * cen_buff) for m in amc),
                    lag_ratio=0.05
                ),
                Write(facts),
                lag_ratio = 0.5
            )
        )
        
        self.wait()

        self.play(
            FadeOut(title, UP),
            FadeOut(amc, DL),
            FadeOut(facts, DR)
        )

class CompFlow(Scene):
    """
    Scene showing progression of American math competitions
    """
    def construct(self):
        t_conf = { "font_size":30 }

        amc = Text("AMC", **t_conf)
        aime = Text("AIME", **t_conf)
        usamo = Text("USAMO", **t_conf)
        imo = Text("IMO", **t_conf)

        comps = VGroup(amc, aime, usamo, imo)
        comps.arrange(RIGHT, buff=2)

        arrs = [ Arrow(a.get_corner(RIGHT), b.get_corner(LEFT), thickness=0.04) for a, b in [(amc, aime), (aime, usamo), (usamo, imo)] ]

        comps.add(*arrs)

        imo_pic = ImageMobject("invariants/assets/imo2015.jpg", height=2)
        imo_pic.next_to(imo, UP, buff=0.5, aligned_edge=DOWN*0.5)

        conf_approx = { "font_size":48, "color":GREY_B, "font": "Fira Code", "weight":"LIGHT" }
        
        app_label = Text("approx no. of\n\nU.S. entrants:", **conf_approx)
        amc_label = Text("~300,000", **conf_approx)
        aime_label = Text("~5,000", **conf_approx)
        usamo_label = Text("~500", **conf_approx)
        imo_label = Text("6", **conf_approx)

        labels = [app_label, amc_label, aime_label, usamo_label, imo_label]
        for label in labels: label.scale(0.2)

        #app_label.next_to(amc, DL, aligned_edge=UR)
        #app_label.shift(LEFT*0.35)

        amc_label.next_to(amc, DOWN)
        aime_label.next_to(aime, DOWN)
        usamo_label.next_to(usamo, DOWN)
        imo_label.next_to(imo, DOWN)

        app_label.next_to(amc_label, LEFT, buff=0.5)

        def arr_anim(i, b, c, grow_kwargs={}, **kwargs):
            return AG( 
                GrowFromEdge(arrs[i], LEFT, **grow_kwargs), 
                AG( Write(b), FadeIn(c), lag_ratio=0.5),
                lag_ratio=0.1,
                **kwargs
            )
        
        self.play(
            FadeIn(app_label),
            AG( Write(amc), FadeIn(amc_label), lag_ratio=0.8 )
        )
        #self.wait()

        self.play(arr_anim(0, aime, aime_label))
        #self.wait()

        self.play(arr_anim(1, usamo, usamo_label))
        #self.wait()

        self.play( 
            arr_anim(2, imo, imo_label),
            FadeIn(imo_pic, DOWN)
        )

        self.wait(1)

        """self.play(
            AG( *(FadeIn(label) for label in labels), lag_ratio=0.1 )
        )"""

class AnotherWay(Scene):
    """
    Scene hinting at the existence of USAMTS
    """
    def construct(self):
        cor_buff = 2
        conf_t = { "font_size": 55, "t2c":{ "3": YELLOW, "15": YELLOW } }

        months = Text("3 months", **conf_t)
        problems = Text("15 problems", **conf_t)
        home = Text("\uf015", font_size=90, font="Font Awesome 5 Free")
        
        home.set_height(home.get_width()*0.85, stretch=True)
        home.scale(1.5)

        r = 3
        pos = lambda n: np.array(( r*cos(2*PI/3 * n + PI/6), r*sin(2*PI/3 * n + PI/6), 0 ))

        months.move_to(pos(0))
        problems.move_to(pos(1))
        home.move_to(pos(2), DOWN)
        
        home.shift(0.5*UP)
        months.shift(0.25*RIGHT)

        alen = 1.5

        self.play(Write(problems, run_time=alen))
        self.wait(0.5)
        self.play(Write(months, run_time=alen))
        self.wait(0.5)
        self.play(Write(home, run_time=alen))
        #self.add(months, problems, home)

class Proof(Scene):
    def construct(self):
        #conf_t = { "font_size":70 }

        catch = Text("The catch?", font_size=70)
        proof = Text("Proof.", gradient=GRAD_A, font_size=90)

        content = VGroup(catch, proof)
        content.arrange(DOWN)

        catch_to_pos = catch.get_center().copy()

        catch.center()

        self.add(catch)
        self.wait()

        self.play(
            AG(
                AG(catch.animate.move_to(catch_to_pos), run_time=0.65),
                Write(proof),
                lag_ratio=0.5
            )
        )

        #self.add(content)

class Intro(Scene):
    """
    Intro which shows f12 logo
    """
    def construct(self):
        axes = Axes(x_range=np.array([-4.0, 4.0, 1.0]), y_range=np.array([-4.0, 4.0, 1.0]), height=6, width=6)

        nx = 10
        ny = 5

        #startsx = [Dot(np.array((i, 0, 0))) for i in range(0, nx)]
        #startsy = [Dot(np.array((0, i, 0))) for i in range(0, ny)]
        #endsx   = [Dot(np.array((i, 0, 0))) for i in range(0, nx)]
        #endsy   = [Dot(np.array((0, i, 0))) for i in range(0, ny)]

        #startsx = Group(*[ValueTracker(0) for i in range(0, nx)])
        #endsx   = Group(*[ValueTracker(0) for i in range(0, nx)])
        #startsy = [ValueTracker(0) for i in range(0, ny)]
        #endsy   = [ValueTracker(0) for i in range(0, ny)]
        #self.add(*startsx, *endsx, *startsy, *endsy)

        #conf_dl = { }

        #linex = lambda i: always_redraw(lambda: DashedLine(axes.c2p(i, startsx[i].get_value(), 0), axes.c2p(i, endsx[i].get_value(), 0), **conf_dl))
        #liney = lambda i: always_redraw(lambda: DashedLine(axes.c2p(i, startsy[i].get_value(), 0), axes.c2p(i, endsy[i].get_value(), 0), **conf_dl))

        #linesx = [linex(i) for i in range(0, nx)]
        #linesy = [liney(i) for i in range(0, ny)]

       # tracker = ValueTracker(0)
        #self.add(tracker)

        #dl = always_redraw(lambda: DashedLine(axes.c2p(0, 0, 0), axes.c2p(0, tracker.get_value(), 0), **conf_dl))
        #self.add(axes, dl)
        #self.add( axes, *linesx)

        #tracker.increment_value(1)
        #tracker.add_updater(lambda m, dt: m.increment_value(dt))
        #self.wait()

        #self.play(tracker.animate.move_to(np.array((0, 3, 0))))

        #endsx[0].increment_value(1)

        f12 = gen_f12()

        self.play(
            Write(f12, rate_func=double_smooth, run_time=4)
        )

        self.play(
            FadeOut(f12, run_time=1)
            #Write(f12, rate_func=(lambda t: smooth(1-t)))
        )

        #self.add(f12)

class USAMTS(Scene):
    """
    Describe the USA Mathematical Talent Search
    """
    def construct(self):
        aopsin = ImageMobject(src("aopsinitiative_bg.png"), height=1.75)
        aops   = ImageMobject(src("aops_logo_bg.png"), height=1)
        wolfram = ImageMobject(src("wolfram_bg"), height=1)
        nsa = ImageMobject(src("nsa_bg.png"), height=2)

        usamts = Text("USAMTS", font_size=50, t2c={"USA":RED})
        usamts.to_edge(LEFT, buff=1)

        rhs = Group(aops, wolfram, nsa)
        rhs.arrange(DOWN, buff=LARGE_BUFF)
        rhs.to_edge(RIGHT, buff=1)

        conf_arr = { "thickness":0.04 }

        rhs_arrs = VGroup(*( Arrow(m.get_corner(LEFT), aopsin.get_corner(RIGHT), **conf_arr) for m in [aops, wolfram, nsa] ))
        lhs_arr = Arrow(aopsin.get_corner(LEFT), usamts.get_corner(RIGHT), **conf_arr)

        an_fade = lambda obj, **kwargs: FadeIn(obj, UP*FADE_BUFF/2, run_time=0.7, **kwargs)
        an_arr = lambda obj, i, **kwargs: AG( an_fade(obj, **kwargs), GrowArrow(rhs_arrs[i]), lag_ratio=0.3 )

        self.play( an_fade(aopsin) )
        self.wait(0.5)
        self.play( an_arr(aops, 0) )
        self.play( an_arr(wolfram, 1) )
        self.play( an_arr(nsa, 2) )
        self.wait(0.5)
        self.play(AG(
            GrowArrow(lhs_arr, run_time=0.5),
            Write(usamts, run_time=1.5),
            lag_ratio=0.3
        ))
        self.wait(1)
        
        #self.play(Write(usamts))

        self.play(usamts.animate.to_corner(UP),  FadeOut(Group(rhs, rhs_arrs, lhs_arr, aopsin)))

        usamts_ul = Underline(usamts)
        g_usamts = VGroup(usamts, usamts_ul)
        self.play(ShowCreation(usamts_ul))

        usr = Group(*[ImageMobject(src("usamts_r{}.png".format(i)), height=4) for i in [1, 2, 3]])
        usr.arrange(RIGHT, buff=LARGE_BUFF)
        usr.shift(DOWN)

        self.play(AG(
            *(FadeIn(m, UP, run_time=1.5) for m in usr),
            lag_ratio=0.2
        ))

        self.wait(1)

        self.play(AG(
            *(FadeOut(m, UP, run_time=1) for m in usr),
            lag_ratio=0.2
        ))

        #usp_easy = ImageMobject(src("usamts_peasy.png"), height=2)
        #usp_hard = ImageMobject(src("usamts_phard.png"), height=0.7)

        conf_tex = {"font_size":20}
        usp_easy = TexText("\\textbf{1/1/31.  } Partition  the grid into 1 by 1 squares and 1 by 2\n\ndominoes in either orientation, marking dominoes with a\n\nline connecting the two adjacent squares, and 1 by 1 squares\n\nwith an asterisk ($\\ast$). No two 1 by 1 squares can share a side.\n\nA \\textit{border} is a grid segment between two adjacent squares\n\nthat contains dominoes of opposite orientations $\\ldots$", **conf_tex)
        usp_hard = TexText("\\textbf{5/1/31.  } Let $n$ be a positive integer. For integers $a, b$ with $0 \\leq a, b \\leq n-1$, let $r_n(a, b)$ denote the remainder when $ab$ is divided by $n$. If $S_n$ denotes the sum of all $n^2$ remainders $r_n(a, b)$ prove that $$\\frac{1}{2} - \\frac{1}{\\sqrt{n}} \\leq \\frac{S_n}{n^3} \\leq \\frac{1}{2}$$", **conf_tex)

        usp = Group(usp_easy, usp_hard)
        usp.arrange(RIGHT, buff=LARGE_BUFF)

        self.play(AG(
            *(FadeIn(m, UP, run_time=1.5) for m in usp),
            lag_ratio=0.7
        ))

        self.wait(2)

        self.play(AG(
            *(FadeOut(m, UP, run_time=1) for m in usp),
            lag_ratio=0.7
        ))

        f12 = gen_f12()
        center_buff = 3
        f12.shift(LEFT * center_buff)

        self.play(Write(f12))

        #self.add(aopsin, rhs, rhs_arrs, lhs_arr, usamts)

class ProblemStatement(Scene):
    """
    Exhibit main problem statement from USAMTS 2019
    """
    def construct(self):
        conf_f = { "font_size":23 }

        YELLOW
        line1 = Text("4/1/31.   A group of 100 friends stands in a circle. Initially, one person has 2019 mangos,\n\n\tand no one else has mangos. The friends split the mangos according to the following rules:", t2w={"4/1/31.":"BOLD"}, **conf_f)
        line2 = Text("\t\t• sharing:  to share, a friend passes two mangos to the left and one mango to the right.", t2s={"sharing":ITALIC}, **conf_f)
        line3 = Text("\t\t• eating:  the mangos must also be eaten and enjoyed.  However, no friend wants to be\n\n\t\tselfish and eat too many mangos.  Every time a person eats a mango, they must also\n\n\t\tpass another mango to the right.", t2s={"eating":ITALIC, **conf_f}, **conf_f)
        line4 = Text("\t\tA person may only share if they have at least three mangos, and they may only eat if they\n\n\thave at least two mangos.  The friends continue sharing and eating, until so many mangos\n\n\thave been eaten that no one is able to share or eat anymore.\n\n\t\tShow that there are exactly eight people stuck with mangos, which can no longer be\n\n\tshared or eaten.", **conf_f)

        text = VGroup(line1, line2, line3, line4)
        text.arrange(DOWN, buff=0.5)

        regs = [ line1[12:52], line1[79:91], line2[3:12], line2[40:90], line3[3:11], line3[145:158], line3[174:207], line4[250:] ]
        
        regs_obj = [ VGroup(*m) for m in regs ]
        conf_style = { "color":BOX_C }

        ul_friends = Underline(regs_obj[0], **conf_style)
        box_sharing = SurroundingRectangle(regs_obj[2], **conf_style)
        box_eating = SurroundingRectangle(regs_obj[4], **conf_style)
        ul_sharing_desc = Underline(regs_obj[3], **conf_style)
        ul_eating_desc1 = Underline(regs_obj[5], **conf_style)
        ul_eating_desc2 = Underline(regs_obj[6], **conf_style)
        box_2019 = SurroundingRectangle(regs_obj[1], **conf_style)
        box_show = SurroundingRectangle(regs_obj[7], **conf_style)

        ul_eating_desc2.set_width(4.5, about_edge=LEFT)

        anim = lambda obj, **kwargs: ShowCreationThenDestruction(obj, **kwargs)
        wait = lambda: self.wait(0.5)

        self.play(Write(text))
        wait()

        self.play( anim(ul_friends))
        wait()
        self.play( anim(box_sharing) )
        self.play( anim(box_eating) )
        wait()
        self.play( anim(ul_sharing_desc) )
        wait()
        self.play( AG(anim(ul_eating_desc1), anim(ul_eating_desc2), lag_ratio=0.2) )
        wait()
        self.play( anim(box_2019) )
        wait()
        self.play( anim(box_show) )

        #self.play( FadeOut(VGroup(*line1[12:45])) )

        #self.embed()

        #self.play(*(Write(line) for line in text))
        #self.add(text)

class SmallExample(Scene):
    def construct(self):
        circ = FriendCircle(3, [5, 0, 0], friend_size=5, radius=1.6)
        circ.gen_rand_state()
        self.add(circ)

        t_val = ValueTracker(0)
        t = lambda: t_val.get_value()
        self.add(t_val)

        circ.add_updater(lambda m: m.anim_states(t()))

        self.wait(1)

        rate = 1/2
        t_val.add_updater(lambda m, dt: m.increment_value(dt*rate))
        self.wait( circ.nstates()/rate )

        self.wait(1)

        self.play(
            *(ShowCreationThenFadeOut(SurroundingRectangle(m, color=BOX_C), run_time=1.5) for m in circ.counters),
        )

        self.embed()

class MedExample(Scene):
    def construct(self):
        circ = FriendCircle(5, [7, 0, 0, 0, 0], friend_size=5, radius=2)
        circ.gen_rand_state()
        self.add(circ)

        t_val = ValueTracker(0)
        t = lambda: t_val.get_value()
        self.add(t_val)

        circ.add_updater(lambda m: m.anim_states(t()))

        self.wait(1)

        rate = 0.7
        t_val.add_updater(lambda m, dt: m.increment_value(dt*rate))
        self.wait( circ.nstates()/rate )

class BeautifulMathAhead(Scene):
    def construct(self):
        sign_color = "#FA6405"

        exterior = Square(3.1, stroke_width=0, fill_color=sign_color, fill_opacity=1)
        interior = Square(2.9, stroke_width=5, stroke_color=BLACK)
        body = VGroup(exterior, interior)
        body.rotate(PI/4)
        body.scale(1.5)

        conf_text = {"font":"Roadgeek 2014 Series D", "font_size":55, "color":BLACK}
        text = VGroup(*( Text(s, **conf_text) for s in ["BEAUTIFUL", "MATH", "AHEAD"] ))

        text.arrange(DOWN, buff=0.6)
        text.shift(DOWN*0.15)

        self.play(AG(
            Write(exterior, stroke_color=sign_color, run_time=2, rate_func=double_smooth),
            AG(
                Write(interior, stroke_color=BLACK, rate_func=smooth, run_time=2),
                Write(text, stroke_color=BLACK, rate_func=smooth, run_time=2.5),
                lag_ratio=0.001
            ),
            lag_ratio=0.5
        ))

        #self.remove(*self.mobjects)

        self.wait(2)
        #self.add(body, text)

bfc_args = { "friend_size":3, "radius":2.5 }
bfc = lambda: FriendCircle(12, [2019, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], **bfc_args)

class BigInitialExample(Scene):
    def construct(self):
        circ = bfc()
        circ.gen_rand_state()
        self.add(circ)

        t_val = ValueTracker(0)
        t = lambda: t_val.get_value()
        self.add(t_val)

        circ.add_updater(lambda m: m.anim_states(t()))

        self.wait(0.5)

        #self.play(FadeOut(circ.counters[1]))

        rate = 251
        t_val.add_updater(lambda m, dt: m.increment_value(dt*rate))
        self.wait( (circ.nstates())/rate )

        self.wait(2)

        rate = 1/2
        t_val.set_value(1000)
        self.wait(30)

        rate = 1/2
        t_val.set_value(circ.nstates() - 12)
        self.wait(30)

        pause = Text("\uf04c", font_size=90, font="Font Awesome 5 Free")
        self.play(Write(pause))
        self.wait(3)
        self.play(FadeOut(pause))

        #t_val.set_value(circ.nstates())
        self.wait(0.1)
        self.play(circ.animate.scale(0.9, about_point=np.array((0, FRAME_Y_RADIUS, 0))))

        self.wait(0.1)

        lhs = Tex("11111100011_2", isolate=["0", "1"])
        rhs = Tex("= 2019", color=SEC_C)
        
        eq = VGroup(lhs, rhs)
        eq.arrange(RIGHT)
        eq.to_edge(DOWN)

        #self.embed()

        self.play(AG(
            *(FadeTransform(m.copy(), lhs[10 - i]) for i, m in enumerate(circ.counters[:11])),
            Write(lhs[11]),
            lag_ratio=0.05,
            run_time=2
        ))

        self.wait(0.5)

        self.play(Write(rhs, run_time=2))

class BigInitialExampleExport(Scene):
    def construct(self):
        circ = bfc()
        circ.gen_rand_state()
        self.add(circ)

        t_val = ValueTracker(0)
        t = lambda: t_val.get_value()
        self.add(t_val)

        circ.add_updater(lambda m: m.anim_states(t()))

        self.wait(0.5)

        #self.play(FadeOut(circ.counters[1]))

        self.play(t_val.animate.increment_value(5), run_time=5, rate_func=linear)

        fast = Text("\uf050", font_size=100, font="Font Awesome 5 Free")
        fast.to_corner(UR)

        bez_w = 50
        self.play(AG(t_val.animate.increment_value(circ.nstates()), run_time=10, rate_func=bezier([*np.full(bez_w, 0), *np.full(bez_w, 1)])), Write(fast))

        #t_val.set_value(circ.nstates())
        #self.wait(0.1)
        self.play(FadeOut(fast), circ.animate.scale(0.9, about_point=np.array((0, FRAME_Y_RADIUS, 0))))

        self.wait(0.1)

        lhs = Tex("11111100011_2", isolate=["0", "1"])
        rhs = Tex("= 2019", color=SEC_C)
        
        eq = VGroup(lhs, rhs)
        eq.arrange(RIGHT)
        eq.to_edge(DOWN)

        #self.embed()

        self.play(AG(
            *(FadeTransform(m.copy(), lhs[10 - i]) for i, m in enumerate(circ.counters[:11])),
            Write(lhs[11]),
            lag_ratio=0.05,
            run_time=2
        ))

        self.wait(0.5)

        self.play(Write(rhs, run_time=2))

        self.wait(2)

class OtherCalcs(Scene):
    def construct(self):
        circ = bfc()
        circ.gen_rand_state()
        self.add(circ)

        t_val = ValueTracker(0)
        t = lambda: t_val.get_value()
        self.add(t_val)

        circ.add_updater(lambda m: m.anim_states(t()))

        self.wait(0.5)

        self.play( t_val.animate.increment_value(circ.nstates()+2), run_time=3, rate_func=smooth )

        #self.wait( (circ.nstates()+2)/rate )

class Why(Scene):
    def construct(self):
        why = Text("Why?", font_size=100)

        self.play(Write(why))

class Explanation(Scene):
    def construct(self):
        conf_f = { "font_size":60 }

        binary = Tex("{{a_n \\cdots a_2 a_1 a_0}}_2", isolate=["a_0", "a_1", "a_2", "a_n"], **conf_f)
        expansion = Tex("= 2^0 a_0 + 2^1 a_1 + 2^2 a_2 + \\ldots", isolate=["a_0", "a_1", "a_2", "=", "\\ldots"], **conf_f)
        summation = Tex("= \sum_{{i = 0}}^n 2^i a_i", color=SEC_C, isolate=["=", "a_i"])

        overline = Underline(VGroup(binary[0], binary[4]))
        overline.next_to(binary, UP, buff=0.2)
        overline.shift(LEFT * 0.15)
        binary.add(overline)

        summation[0].set_color(WHITE)

        ex = VGroup(binary, expansion, summation)
        ex.arrange(ORIGIN, buff=0.5, aligned_edge=LEFT)
        shift_amt = 1

        self.play(Write(binary))
        self.wait(0.5)

        self.play( binary.animate.shift(UP * shift_amt) )

        self.play(
            #Write(expansion[0]),
            FadeTransform(binary[4].copy(), expansion[2]),
            FadeTransform(binary[3].copy(), expansion[4]),
            FadeTransform(binary[2].copy(), expansion[6]),
            FadeTransform(binary[0].copy(), expansion[8]),
            Write(VGroup(expansion[0], expansion[1], expansion[3], expansion[5], expansion[7])),
            run_time=1.5
        )
        self.wait(0.5)

        self.play( VGroup(binary, expansion).animate.shift(UP * (shift_amt +  0.3)) )

        self.play(
            Write(summation),
            *(FadeTransform(expansion[i].copy(), summation[-1]) for i in [2, 4, 6])
        )
        self.wait(0.5)

        removal = VGroup(binary, expansion, summation[0])
        thesum = summation[1:]   

        #friend circle
        circ = bfc()
        circ.gen_rand_state()
        self.add(circ)

        t_val = ValueTracker(0)
        t = lambda: t_val.get_value()
        self.add(t_val)

        circ.scale(0.9, about_point=np.array((0, FRAME_Y_RADIUS, 0)))
        circ.shift(0.5*UP)

        circ.add_updater(lambda m: m.anim_states(t()))

        self.play(
            FadeOut(removal),
            thesum.animate.to_corner(DL),
            FadeIn(VGroup(circ.circle, *circ.friends, *circ.counters), run_time=3),
            run_time=2
        )

        #self.add(ex)

class Test(Scene):
    def construct(self):
        axes = Axes()

        dot = Dot(np.array((0, 0, 0)))
        dot2 = Dot(np.array((0, 1, 0)))

        dl = always_redraw(lambda: DashedLine(axes.c2p(*dot.get_center()), axes.c2p(*dot2.get_center())))

        self.add(axes, dot, dot2, dl)

        
        self.play(dot.animate.move_to(np.array((1, 0, 0))))

        #conf_approx = { "font_size":48, "color":GREY_B, "font": "Fira Code", "weight":"LIGHT" }
        #app_label = Text("""approx no. of\n\nU.S. entrants""", width=10, **conf_approx)
        #app_label.set_width(1)

        #self.add(app_label)