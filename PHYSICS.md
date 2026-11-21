# Physics Behind the Lander
So this is basically all the math behind the simulator. For the rocket stuff (sections 1–4) I followed the derivations from NASA Glenn Research Center's [Guide to Rockets](https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/guide-to-rockets/), I didn't come up with these myself, but I went through all of them by hand so I actually get where everything comes from instead of just plugging in formulas. My notes are scanned in each section. Sections 5–8 are the parts I had to figure out for my own simulation.

## 1. Thrust

  So force is F = ma, which is also F = m(dv/dt), which is also $F = \frac{dp}{dt}$ where p is momentum. For a rocket the momentum is coming from all the mass shooting out the nozzle, so that's where the first part of the thrust equation comes from. The second part comes from pressure, since P = F/A you just do some algebra and get F = PA, and that's where the pressure term comes from:

  $$F = \dot m V_e + A_e(P_e - P_0)$$

  - $\dot m$ = mass flow rate, basically how much exhaust mass leaves every second
  - $V_e$ = exhaust velocity
  - $A_e$ = area of the nozzle exit
  - $P_e$ = pressure of the exhaust, $P_0$ = surrounding pressure

  On the Moon there's pretty much no atmosphere so $P_0 = 0$, which makes it simpler.

  <img width="500" alt="03_thrust" src="https://github.com/user-attachments/assets/284bf2b1-c83c-4325-b4c4-5a249a6c0f44" />

## 2. Mass flow rate

  This one comes from conservation of mass, the rate mass goes into a spot has to be the same rate it leaves, so the mass flow rate stays constant:

  $$\dot m = \rho A V$$

  $\rho$ is the density, $A$ is the area and $V$ is the velocity.

## 3. Specific impulse

  You can kinda fold the pressure part into one "equivalent" exhaust velocity:

  $$V_{eq} = V_e + \frac{A_e(P_e - P_0)}{\dot m}$$

  which makes thrust just $F = \dot m V_{eq}$. Then specific impulse is just that velocity divided by Earth's gravity:

  $$I_{sp} = \frac{V_{eq}}{g_0}$$

  I use $g_0 = 9.80665\ \text{m/s}^2$ even though the lander is on the Moon, because Isp was defined using Earth's gravity, not the Moon's.

  **This is the formula my code actually uses:**

  $$F = I_{sp}\, g_0\, \dot m \qquad\Longleftrightarrow\qquad \dot m = \frac{F}{I_{sp}\, g_0}$$

  So the guidance figures out how much thrust it needs, and then this tells me how fast the fuel has to burn to get that thrust. I used Isp = 311 s which is Apollo's descent engine.

  <img width="500" alt="04_mass_flow_and_specific_impulse" src="https://github.com/user-attachments/assets/f86f8c59-e8b2-46bb-9763-58f7a1491142" />

## 4. Ideal rocket equation (background)

  If you do conservation of momentum on the rocket and the exhaust you end up with:

  $$\Delta u = V_{eq}\ln\left(\frac{m_0}{m_f}\right)$$

  and if gravity is pulling on it during a burn that lasts $t_b$:

  $$\Delta u = V_{eq}\ln\left(\frac{m_0}{m_f}\right) - g\,t_b$$

  My simulation doesn't actually use this equation since it just steps through time, but this is basically the reason the changing mass matters so much.

  <img width="500" alt="01_ideal_rocket_equation" src="https://github.com/user-attachments/assets/bca87164-4f59-4a58-b3b2-bc727296b6da" />
  <img width="500" alt="02_ideal_rocket_equation_continued" src="https://github.com/user-attachments/assets/9ea4a9e9-57fa-4860-8556-e087e41504b4" />

## 5. Guidance law

  The whole idea was to get the lander to slow down so it hits the ground at basically 0 velocity. So I used the kinematics equation:

  $$v_f^2 = v^2 + 2a\,\Delta x$$

  The final velocity is 0, and since the lander is going down by its altitude h, $\Delta x = -h$. So:

  $$0 = v^2 - 2ah \quad\Longrightarrow\quad a = \frac{v^2}{2h}$$

  The negative from $\Delta x$ cancels out so a comes out positive, which is just an upward deceleration. Then I used Newton's second law to get the thrust (up is positive):

  $$F_{thrust} - mg = ma \quad\Longrightarrow\quad F_{thrust} = m(g + a)$$

  The guidance recalculates this every single step with whatever the current velocity, altitude and mass are.

  <img width="500" alt="05_guidance_logic" src="https://github.com/user-attachments/assets/5dbbb9da-3ba0-4269-8d6c-24f03ac7c695" />
  <img width="500" alt="06_guidance_idea_and_parameters" src="https://github.com/user-attachments/assets/b8537d6d-ed59-42df-a1ca-dd5480360e01" />

## 6. Euler's method

  Every time step ($\Delta t = 0.02$ s) the code just updates everything:

  $$m_{n+1} = m_n - \dot m\,\Delta t$$

  $$v_{n+1} = v_n + a_n\,\Delta t$$

  $$h_{n+1} = h_n + v_{n+1}\,\Delta t$$

  The mass can't go below the lander's empty mass, cuz you can't burn fuel you don't have.

## 7. Engine cutoff and free fall

  Once the lander is under 1.7 m and going slower than 1 m/s, I set the thrust to 0 and let it free fall with lunar gravity ($g = 1.625\ \text{m/s}^2$). The height while it's falling is:

  $$h(t) = h_0 + v_0 t - \tfrac12 g t^2$$

  If you set h = 0 and solve the quadratic you get how long it falls, and the speed it hits the ground at is:

  $$v_{impact} = \sqrt{v_0^2 + 2 g h_0}$$

  If $v_{impact} < 3.05$ m/s, which is what the lunar module's landing gear was designed for, it counts as a safe landing.

## 8. Checking the simulation

  Since the guidance law keeps the deceleration constant, the whole descent should line up with the exact constant acceleration solution:

  $$h(t) = h_0 + v_0 t + \tfrac12 a t^2, \qquad v(t) = v_0 + a t$$

  With $h_0 = 213.4$ m and $v_0 = -6.4$ m/s:

  $$a = \frac{6.4^2}{2(213.4)} \approx 0.096\ \text{m/s}^2, \qquad t_{land} = \frac{2h_0}{|v_0|} \approx 66.7\ \text{s}$$

  The acceleration in my sim stays at around 0.096 m/s² the whole way down so it matches. This was honestly super useful cuz the code spits out a ton of numbers and there's no way I'm checking every step by hand.


## Parameters

| Parameter | Value |
|---|---|
| Lunar gravity | 1.625 m/s² |
| Earth gravity ($g_0$) | 9.80665 m/s² |
| Specific impulse | 311 s |
| Empty mass | 4,214 kg |
| Starting mass | 15,065 kg |
| Surrounding pressure | 0 |
| Time step | 0.02 s |
| Starting altitude | 213.4 m (700 ft) |
| Starting velocity | -6.4 m/s (21 ft/s down) |
