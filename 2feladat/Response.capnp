@0xc006e8d67841eca5;

# using Java = import "java.capnp";
# $Java.package("org.ericsson2017.protocol.semifinal");
# $Java.outerClassname("ResponseClass");

# using Cxx = import "/capnp/c++.capnp";
# $Cxx.namespace("ericsson2017::protocol::semifinal");


using Common = import "Common.capnp";


struct Cell {
    owner @0 : Int32;
    attack : union {
        can @1 : Bool = true;
        unit @2 : Int32;
    }
}

struct Enemy {
    position @0 : Common.Position;
    direction : group {
        vertical @1 : Common.Direction;
        horizontal @2 : Common.Direction;
    }
}

struct Unit {
    owner @0 : Int32;
    position @1 : Common.Position;
    direction @2 : Common.Direction;
    health @3 : Int32 = 3;
    killer @4 : Int32 = 6;
}

struct Response {
    status @0 : Text;
    info : group {
        owns @1 : Int32;
        level @2 : Int32;
        tick @3 : Int32;
    }
    cells @4 : List(List(Cell));
    enemies @5 : List(Enemy);
    units @6 : List(Unit);
}

