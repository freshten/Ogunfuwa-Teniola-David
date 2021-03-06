# ... to the only wise God

# This is the home of functions that implements simple petroleum engineering computations.

######## A function to compute real gas density ########
# Note: pressure must be in psia and temperature in degree Rankine

def gas_density(gravity, pressure = 14.7, temperature = 520, z = 1):
    density = (2.70*pressure*gravity)/(z*temperature)
    return round(density, 4)



######## A function to estimate bubble point pressure, pb ########
# Note: this function only works if solution gas-oil ratio at a pressure above bubble point (i.e. Rsi (=Rsb)) is known
# Note that temperature is in degree Fahreiheit

def bubble_pressure(temperature, pressure, gas_gravity, oil_gravity, rsb): 
    api = (141.5/oil_gravity)-131.5
    y = (0.00091*temperature)-(0.0125*api)
    pb = (18*(10**y))*((rsb/gas_gravity)**0.83)
    return round(pb,2)



######## A function to compute solution gas-oil ratio, Rs ########
# Note: temperature must be in degree Fahreiheit

def sol_gor(temperature, pressure, gas_gravity, oil_gravity, pb): # where pb is bubble point pressure.
    api = (141.5/oil_gravity)-131.5
    y = (0.00091*temperature)-(0.0125*api)
    if pressure<pb:
        rs = gas_gravity*(((pressure)/(18*(10**y)))**1.205)
        return round(rs,2)
    else:
        rsb = gas_gravity*(((pb)/(18*(10**y)))**1.205)
        return round(rsb,2)


########  A function to compute oil formation volume factor, Bo ########
# Note: temperature must be in degree Fahreiheit
# For pressures above or at bubble point, either pb or rs may be skipped; but not both.
# For pressures below bubble point, only rs may be skipped.
# co is required if pressure is above bubble point; otherwise, it must be skipped.
# A few notes about defaulted parameters pb, rs and co.
    # They are defaulted - hence, users ma skip them when specifying argument values.
    # They are defaulted to None (nothing). So, if a user skip them, what value is used?
    # For co:
            # co is truly optional!
            # It is only needed if value specified for argument pressure is greater than value specified for argument pb
            # If pressure is greater than pb, it is expected that the user has specified value for co
                # That specified co value overides the default value (None) and get used in the computation
            # If pressure is equal to or less than pb, it is expected that the user has not specified value for co
                # In this case, the function does not need co in computation
                # So, co remained defaulted to None and is never used in computation.
    # For pb and rs:
            # They are only optional in the context of argument specification
            # In usage, they are not optional, the function need their values
            # If a user specify their values, the specified value(s) overides the default (None) and get used in computation.
            # If a user did not specify their values, function fvf itself computes their velues internally by calling functions bubble_pressure and sol_gor
            # Functions bubble_pressure and sol_gor are also defined in here in peteng.py
            # The internally-computed values of pb and rs then overides the default values (None) and get used in computation.

def fvf(pressure, temperature, gas_gravity, oil_gravity, pb = None, rs = None, co = None):
    
    # calling function bubble_pressure if neccessary (i.e. if pb is not specified)
    if pb is None:
        pb = bubble_pressure(temperature, pressure, gas_gravity, oil_gravity, rs)

    # calling function sol_gor if neccessary (i.e. if rs is not specified)
    if rs is None:
        rs = sol_gor(temperature, pressure, gas_gravity, oil_gravity, pb)

    # calculating F parameter
    F = (rs*((gas_gravity/oil_gravity)**0.5))+(1.25*temperature)

    if pressure > pb:
        bob = 0.9759+(0.00012*(F**1.2)) # assuming gas_gravity and oil_gravity are constant for all pressures above pb
        # importing needed library
        import math
        bo = bob*(math.exp(co*(pb-pressure)))
    else:
        bo = 0.9759+(0.00012*(F**1.2))

    return round(bo, 4)



########  A function to compute Stock Tank Oil Initially In-Place (STOIIP), N ########
def stoiip(area, thickness, poro, sw, boi):
    N = (7758*area*thickness*poro*(1-sw))/boi
    return round(N, 2)
    
