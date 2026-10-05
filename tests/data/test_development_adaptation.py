import pytest
from benchmarks.byt5_development_adaptation import admit, distance, validate_recipe


def test_exact_bounded_recipes_and_native_capacity():
    validate_recipe(.0003,"",600)
    validate_recipe(.0001,"Restore transcript: ",600)
    for lr,prefix,n in ((.0003,"Restore transcript: ",600),(.0001,"",600),(.0003,"",601)):
        with pytest.raises(ValueError):validate_recipe(lr,prefix,n)
    admit({"source":"x"*511,"reference":"é"*255})
    with pytest.raises(ValueError):admit({"source":"Restore transcript: "+"x"*500,"reference":"x"})
    with pytest.raises(ValueError):admit({"source":"x","reference":"é"*256})


def test_lexical_distance_preserves_insertions_and_normalization():
    assert distance("A naïve command.","a naïve command")==0
    assert distance("one two","one four two")==1
    assert distance("one two","")==2
