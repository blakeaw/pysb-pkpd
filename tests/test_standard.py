from pysb.pkpd import standard


def test_one_compartment_model():
    model_1 = standard.one_compartment_model(dose_amount=100.0)
    assert len(model_1.parameters) == 3
    assert len(model_1.rules) == 1
    assert len(model_1.expressions) == 2
    assert len(model_1.initials) == 1
    assert len(model_1.monomers) == 1
    assert len(model_1.compartments) == 1
    for key in standard.PD_MODELS.keys():
        kwargs = dict()
        for item in standard.PD_MODEL_ARGS[key]:
            kwargs[item] = 1.0
        model_1 = standard.one_compartment_model(
            dose_amount=100.0, pd_model={key: kwargs}
        )
        assert len(model_1.parameters) == 3 + len(standard.PD_MODEL_ARGS[key])
        assert len(model_1.rules) == 1
        assert len(model_1.expressions) == 3
        assert len(model_1.initials) == 1
        assert len(model_1.monomers) == 1
    for key in standard.DOSING_OPTIONS.keys():
        model_1 = None
        if key == "oral":
            model_1 = standard.one_compartment_model(
                dose_amount=100.0,
                dose_route=key,
                dose_parameters={"ka": 1e-2, "f": 0.75},
            )
        else:
            model_1 = standard.one_compartment_model(dose_amount=100.0, dose_route=key)

        if key == "oral":
            assert len(model_1.parameters) == 5
            assert len(model_1.expressions) == 3
            assert len(model_1.rules) == 2
            assert len(model_1.initials) == 1
            assert len(model_1.monomers) == 2
        elif key == "iv-infusion":
            assert len(model_1.parameters) == 3
            assert len(model_1.expressions) == 2
            assert len(model_1.rules) == 2
            assert len(model_1.initials) == 0
            assert len(model_1.monomers) == 1
        else:
            assert len(model_1.parameters) == 3
            assert len(model_1.expressions) == 2
            assert len(model_1.rules) == 1
            assert len(model_1.initials) == 1
            assert len(model_1.monomers) == 1

def test_two_compartment_model():
    model_2 = standard.two_compartment_model(dose_amount=100.0)
    assert len(model_2.compartments) == 2
    assert len(model_2.parameters) == 6
    assert len(model_2.rules) == 2
    assert len(model_2.expressions) == 2
    assert len(model_2.initials) == 1
    assert len(model_2.monomers) == 1
    for key in standard.PD_MODELS.keys():
        kwargs = dict()
        for item in standard.PD_MODEL_ARGS[key]:
            kwargs[item] = 1.0
        model_2 = standard.two_compartment_model(
            dose_amount=100.0, pd_model={key: kwargs}
        )
        assert len(model_2.parameters) == 6 + len(standard.PD_MODEL_ARGS[key])
        assert len(model_2.rules) == 2
        assert len(model_2.expressions) == 3
        assert len(model_2.initials) == 1
        assert len(model_2.monomers) == 1
    for key in standard.DOSING_OPTIONS.keys():
        model_2 = None
        if key == "oral":
            model_2 = standard.two_compartment_model(
                dose_amount=100.0,
                dose_route=key,
                dose_parameters={"ka": 1e-2, "f": 0.75},
            )
        else:
            model_2 = standard.two_compartment_model(dose_amount=100.0, dose_route=key)

        if key == "oral":
            assert len(model_2.parameters) == 8
            assert len(model_2.expressions) == 3
            assert len(model_2.rules) == 3
            assert len(model_2.initials) == 1
            assert len(model_2.monomers) == 2
        elif key == "iv-infusion":
            assert len(model_2.parameters) == 6
            assert len(model_2.expressions) == 2
            assert len(model_2.rules) == 3
            assert len(model_2.initials) == 0
            assert len(model_2.monomers) == 1
        else:
            assert len(model_2.parameters) == 6
            assert len(model_2.expressions) == 2
            assert len(model_2.rules) == 2
            assert len(model_2.initials) == 1
            assert len(model_2.monomers) == 1

def test_three_compartment_model():
    model_3 = standard.three_compartment_model(dose_amount=100.0)
    assert len(model_3.compartments) == 3
    assert len(model_3.parameters) == 9
    assert len(model_3.rules) == 3
    assert len(model_3.expressions) == 2
    assert len(model_3.initials) == 1
    assert len(model_3.monomers) == 1
    for key in standard.PD_MODELS.keys():
        kwargs = dict()
        for item in standard.PD_MODEL_ARGS[key]:
            kwargs[item] = 1.0
        model_3 = standard.three_compartment_model(
            dose_amount=100.0, pd_model={key: kwargs}
        )
        assert len(model_3.parameters) == 9 + len(standard.PD_MODEL_ARGS[key])
        assert len(model_3.rules) == 3
        assert len(model_3.expressions) == 3
        assert len(model_3.initials) == 1
        assert len(model_3.monomers) == 1
    for key in standard.DOSING_OPTIONS.keys():
        model_3 = None
        if key == "oral":
            model_3 = standard.three_compartment_model(
                dose_amount=100.0,
                dose_route=key,
                dose_parameters={"ka": 1e-2, "f": 0.75},
            )
        else:
            model_3 = standard.three_compartment_model(dose_amount=100.0, dose_route=key)

        if key == "oral":
            assert len(model_3.parameters) == 11
            assert len(model_3.expressions) == 3
            assert len(model_3.rules) == 4
            assert len(model_3.initials) == 1
            assert len(model_3.monomers) == 2
        elif key == "iv-infusion":
            assert len(model_3.parameters) == 9
            assert len(model_3.expressions) == 2
            assert len(model_3.rules) == 4
            assert len(model_3.initials) == 0
            assert len(model_3.monomers) == 1
        else:
            assert len(model_3.parameters) == 9
            assert len(model_3.expressions) == 2
            assert len(model_3.rules) == 3
            assert len(model_3.initials) == 1
            assert len(model_3.monomers) == 1

if __name__ == "__main__":
    test_one_compartment_model()
    test_two_compartment_model()
    test_three_compartment_model()
