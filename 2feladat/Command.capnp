@0xabf8f53c554fa923;

# using Java = import "java.capnp";
# $Java.package("org.ericsson2017.protocol.semifinal");
# $Java.outerClassname("CommandClass");

# using Cxx = import "/capnp/c++.capnp";
# $Cxx.namespace("ericsson2017::protocol::semifinal");


using Common = import "Common.capnp";

struct Move {
    unit @0 : Int32;
    direction @1 : Common.Direction;
}

struct Command {
    commands : union {
        moves @0 : List(Move);
        login : group {
            team @1 : Text;
            hash @2 : Text;
        }
    }
}
