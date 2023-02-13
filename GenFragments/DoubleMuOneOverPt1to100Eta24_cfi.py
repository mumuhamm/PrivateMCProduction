import FWCore.ParameterSet.Config as cms

generator = cms.EDProducer("FlatRandomOneOverPtGunProducer",
    PGunParameters = cms.PSet(
        MinOneOverPt = cms.double(1/100.0),
        MaxOneOverPt = cms.double(1/1.5),
        PartID = cms.vint32(13),
        MaxEta = cms.double(2.4),
        MaxPhi = cms.double(3.14159265359),
        MinEta = cms.double(-2.4),
        MinPhi = cms.double(-3.14159265359) ## in radians

    ),
    Verbosity = cms.untracked.int32(0), ## set to 1 (or greater)  for printouts

    psethack = cms.string('double mu pt 1-100'),
    AddAntiParticle = cms.bool(True),
    firstRun = cms.untracked.uint32(1)                           
)
