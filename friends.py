from manimlib import *
from itertools import product
from math import cos, sin, floor
from numpy.random import choice

BG_COLOR = "#181818"
MANGO_COLOR = GOLD_D

class PiecewiseInterpolate(object):
    def __init__(self, stages, interp=lambda t: t):
        self.stages = stages
        self.interp = interp
        self.cutoff = False

    def __call__(self, t):
        t = self.clamp(t)

        times = list(map(lambda m: m["time"], self.stages))
        total_time = sum(times)
        for i, tr in enumerate(times): times[i] /= total_time

        for i, stage in enumerate(self.stages):
            t_bef = sum(times[:i])
            t_af = sum(times[:(i+1)])
            if t >= t_bef and t <= t_af:
                if self.cutoff and i >= self.cutoff: return self.stages[self.cutoff]["start"]
                stagedata = { "start":0, "end":1, "interp": self.interp, "pas": False, **stage }
                if stagedata["pas"]: stagedata["end"] = stagedata["start"]
                return interpolate( stagedata["start"], stagedata["end"], stagedata["interp"]((t - t_bef)/(t_af - t_bef)) )

    def cut(self, i):
        self.cutoff = i
        return self
 
    def clamp(self, t):
        if t >= 1: return 1
        if t <= 0: return 0
        return t

    def copy(self):
        obj = PiecewiseInterpolate(self.stages, self.interp)
        obj.cutoff = self.cutoff
        return obj


class Friend(VGroup):
    CONFIG = {
        "background_color": BG_COLOR,
        "mango_color": MANGO_COLOR,
        "arm_size": 0.4,
        "mango_size": 0.3,
        "stroke_width": 2,
        "size": 1.0
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.axes = Axes()
        cargs = { "stroke_width": self.stroke_width, "radius": self.size, "stroke_color": WHITE, "fill_color": None, "fill_opacity": 0.0 }
        acargs = { "radius": self.size*self.arm_size }
        mcargs = { "radius": self.size*self.mango_size, "stroke_width": 0.0, "fill_color": self.mango_color, "fill_opacity": 1.0 }
        self.body = Circle(**cargs)
        self.arm1 = Circle(**{**cargs, **acargs})
        self.arm2 = Circle(**{**cargs, **acargs})
        self.mango1 = Circle(**mcargs)
        self.mango2 = Circle(**mcargs)
        self.elements = VGroup(self.arm1, self.arm2, self.body, self.mango1, self.mango2, self.axes)
        self.add(self.elements)
        VGroup(self.axes, self.mango1, self.mango2).set_opacity(0)
        self.reset_position()

    # animations

    INTERP_FUNC = smooth
    IDLE_POS = ((0, 0, 0), ((1.3, -0.72, 0), (-1.3, -0.72, 0)), ((1.6, -1.4, 0), (-1.6, -1.4, 0)))
    SHARE_POS = ((0, 0, 0), ((2, -0.31, 0), (-2, -0.31, 0)), ((2.6, -0.31, 0), (-2.6, -0.31, 0)))
    EAT_POS = ((0, 0, 0),  ((0.6, -0.25, 0), SHARE_POS[1][1]), ( (0.1, 0, 0), SHARE_POS[2][1] ) )

    def reset_position(self):
        self.move(*self.IDLE_POS)

    def anim_share(self, t):
        self.anim_mango(t, self.SHARE_POS)

    def anim_eat(self, t):
        self.anim_mango(t, self.EAT_POS, rhangle=0)

    def anim_mango(self, t, pos_to, rhangle=PI/4, lhangle=-PI/4, pos_from=IDLE_POS):
        pos = ((0, 0, 0), [(0, 0, 0), (0, 0, 0)], [(0, 0, 0), (0, 0, 0)] )

        int_hands = PiecewiseInterpolate([{"time": 1, "pas": True}, 
                                          {"time": 5, "start": 0, "end": 1}, 
                                          {"time": 0.5, "start": 1, "end": 1 }, 
                                          {"time": 3, "start": 1, "end": 0}], smooth)

        int_mango_pos = int_hands.copy().cut(2)

        int_mango_opac = PiecewiseInterpolate([{"time": 2}, 
                                               {"time": 11, "start": 1, "pas": True},
                                               {"time": 2, "start": 1, "end": 0},
                                               {"time": 9, "start": 0, "pas": True}])

        for i, j in product([0, 1], [1, 2]):
            pos[j][i] = (path_along_arc( ([rhangle, lhangle])[i] ))(np.array(pos_from[j][i]),np.array(pos_to[j][i]), ([int_hands(t), int_mango_pos(t)])[j-1])

        for m in self.get_mangos(): m.set_opacity(int_mango_opac(t))
        self.move(*pos)

    # getters, setters

    def c2p(self, *coords):
        return self.get_axes().c2p(*coords)

    def move(self, body=None, arms=None, mangos=None):
        if body: self.get_body().move_to(self.c2p(*body))
        for i in [0, 1]:
            if arms and len(arms) > i: self.get_arms()[i].move_to(self.c2p(*arms[i]))
            if mangos and len(mangos) > i: self.get_mangos()[i].move_to(self.c2p(*mangos[i]))

    def get_axes(self):
        return self.axes

    def get_body(self):
        return self.body

    def get_arms(self):
        return [self.arm1, self.arm2]
    
    def get_mangos(self):
        return [self.mango1, self.mango2]

    def get_main_objs(self):
        return self.get_arms() + self.get_body()

EAT = 0
SHARE = 1

class FriendCircle(VGroup):
    CONFIG = {
        "circle_sw":  2,
        "sw": 2,
        "friend_size": 3.5,
        "text_size": 30,
        "radius": 2,
        "buff": 0.4,
        "p_eat": 0.5
    }

    def __init__(self, n, init_state, **kwargs):
        super().__init__(**kwargs)
        if not len(init_state) == n: raise Exception("Initial state must be of size n")

        self.init_state = init_state
        self.n = n
        self.states = [ ]
        self.circle = Circle(radius=self.radius, stroke_width=self.circle_sw, stroke_color=WHITE)
        #self.ax = Axes()
        #self.ax.scale(1.31)
        #self.ax.set_opacity(0)
        self.friends = VGroup()
        self.counters = VGroup()

        for i in range(0, n):
            ap = self.get_anchor_points()[i]

            f = Friend(stroke_width=self.sw)
            self.friends.add(f)
            f.set_width(self.friend_size)
            ang = (2*PI / n) * i
            f.rotate(ang)
            f.move_to(ap[0])

            counter = Integer(init_state[i], edge_to_fix=ORIGIN, font_size=self.text_size)
            #counter.scale(self.text_size)
            counter.move_to(ap[1])
            counter.shift(0.04 * (self.text_size/30) * DOWN)
            self.counters.add(counter)

        self.add(self.circle, self.friends, self.counters)
        
    def gen_rand_state(self):
        self.clear_states()

        def movable(state):
            return not all(i <= 1 for i in state)

        curr_state = self.init_state
        while movable(curr_state):
            next_state = [ ]
            action = EAT
            #actable_indices = list(map( lambda i, m: i, filter(lambda i, m: m >= 2, enumerate(curr_state))))
            actable_indices = [ ]
            for i, m in enumerate(curr_state): 
                if m >= 2: actable_indices.append(i)

            i = choice(actable_indices)
            if curr_state[i] <= 2 or choice([0, 1], p=[self.p_eat, 1 - self.p_eat]) == 0:
                next_state = self.eat(i, curr_state)
                action = EAT
            else:
                next_state = self.share(i, curr_state)
                action = SHARE
            
            self.add_state([curr_state, [i, action]])
            curr_state = next_state

        self.add_state([curr_state])

    def eat(self, i, state):
        new_state = state.copy()
        new_state[i % self.n] -= 2
        new_state[(i + 1) % self.n] += 1
        return new_state

    def share(self, i, state):
        new_state = state.copy()
        new_state[i % self.n] -= 3
        new_state[(i+1) % self.n] += 1
        new_state[(i-1) % self.n] += 2
        return new_state

    def anim_states(self, t, simul=False):
        if len(self.states) < 2: return

        j = min(floor(t), len(self.states)-2)
        p = min(t - j, 1)

        if t >= len(self.states)-1:
            for f in self.get_friends():
                f.reset_position()
            for i, c in enumerate(self.counters):
                c.set_value(self.states[-1][0][i])
            return

        int_c_down = PiecewiseInterpolate([{"time":1, "start": 0, "end": 1}, 
                                           {"time":2, "start": 1, "end": 1}], smooth)

        int_c_up   = PiecewiseInterpolate([{"time":2, "start": 0, "end": 0}, 
                                           {"time":1, "start": 0, "end": 1}], smooth)

        if simul:
            int_c_up = int_c_down = PiecewiseInterpolate([{"time": 1, "start": 0, "end": 0},
                                                          {"time": 1, "start": 0, "end": 1},
                                                          {"time": 1, "start": 1, "end": 1}], smooth)

        state_from = self.states[j]
        state_to   = self.states[j+1]

        # animate the friend
        fi = state_from[1][0]
        friend = self.get_friend(state_from[1][0])
        for i in range(0, self.n):
            if i == state_from[1][0]:
                ({ EAT:friend.anim_eat, SHARE:friend.anim_share }[state_from[1][1]])(p)
            else:
                self.get_friend(i).reset_position()

        # animate the relevant counters
        cval = lambda i, f: interpolate(state_from[0][i], state_to[0][i], round(f(p)))
        for i in range(0, self.n):
            if i in [(fi-1)%self.n, (fi+1)%self.n]:
                self.counters[i].set_value(cval(i, int_c_up))
            elif i in [fi%self.n]:
                self.counters[i].set_value(cval(i, int_c_down))
            #else:
                #self.counters[i].set_value(state_to[0][i])


    def get_anchor_points(self):
        r = [ ]
        for i in range(0, self.n):
            ang = (2*PI / self.n) * i
            vec = np.array(( cos(ang + PI/2), sin(ang + PI/2), 0 ))
            r.append( [ (self.radius + (self.buff * (self.friend_size/3.5) )) * vec, (self.radius - self.buff) * vec, vec ] )
        return r

    def nstates(self):
        return len(self.states) - 1

    def add_state(self, state):
        self.states.append(state)

    def clear_states(self):
        self.states = [ ]

    def get_friend(self, i):
        return self.get_friends()[i % self.n]

    def get_friends(self):
        return self.friends


class Testing(Scene):
    def construct(self):
        interp = PiecewiseInterpolate([
            {"time": 10, "start": 0, "end": 1},
            {"time": 10, "start": 1, "end": 0}
        ])

        #print(interp(0.75))

        t_val = ValueTracker(0)
        self.add(t_val)

        friend = Friend()
        #friend.add_updater(lambda m: m.anim_eat(t_val.get_value()))
        #t_val.add_updater(lambda m, dt: m.increment_value(dt/2))

        friend.move_to(np.array((2, 2, 0)))

        self.add(friend)

        

class Testing2(Scene):
    def construct(self):
        t_val = ValueTracker(0)
        self.add(t_val)

        friend_circle = FriendCircle(8, [2019, 0, 0, 0, 0, 0, 0, 0], p_eat=0.7)
        friend_circle.gen_rand_state()

        print(friend_circle.states[:4])

        #print(len(friend_circle.states))

        friend_circle.add_updater(lambda m: m.anim_states(t_val.get_value()))
        t_val.add_updater(lambda m, dt: m.increment_value(dt/2))

        self.add(friend_circle)

        self.wait(100)