from subprocess import check_call, DEVNULL
from ase.io.pov import write_pov
from ase.build import molecule
from ase.io.pov import get_bondpairs, set_high_bondorder_pairs


def test_povray_io(povray_executable):
    H2 = molecule('H2')
    write_pov('H2.pov', H2)
    check_call([povray_executable, 'H2.pov'], stderr=DEVNULL)


def test_povray_highorder(povray_executable):

    atoms = molecule('CH4')
    radii = [0.2] * len(atoms)
    bondpairs = get_bondpairs(atoms, radius=1.0)
    assert len(bondpairs) == 4

    high_bondorder_pairs = {}

    def setbond(target, order):
        high_bondorder_pairs[(0, target)] = ((0, 0, 0), order, (0.1, -0.2, 0))

    setbond(2, 2)
    setbond(3, 3)
    bondpairs = set_high_bondorder_pairs(bondpairs, high_bondorder_pairs)

    renderer = write_pov(
        'atoms.pov', atoms,
        generic_projection_settings=dict(radii=radii),
        povray_settings=dict(canvas_width=50, bondatoms=bondpairs))

    # XXX Not sure how to test that the bondpairs data processing is correct.
    pngfile = renderer.render()
    assert pngfile.is_file()
    print(pngfile.absolute())
