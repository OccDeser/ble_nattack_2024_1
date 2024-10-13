# BC Legacy Session Establishment

## Sequence

```mermaid
sequenceDiagram
    participant A as Alice ( Central )
    participant B as Bob ( Peripheral )
 
 Note over A: AddressA: Alice 的地址
 Note over B: AddressB: Bob 的地址
    Note over A,B: Alice and Bob shared the LK

    Note over A: Fresh AuRand <br/> SRES, ACO = E1(LK, AuRand, AddressB)
    A->>B: LMP_AU_RAND { AuRand }
    Note over B: SRES, ACO = E1(LK, AuRand, AddressB)
    B->>A: LMP_SRES { SRES }
    Note over A: Verify SRES

    A->>B: LMP_ENCRYPTION_KEY_SIZE_REQ { KeySize }
    B->>A: LMP_ACCEPTED

    Note over A: Fresh EnRand <br/> SK = Es(E3(LK, EnRand, ACO), KeySize)
    A->>B: LMP_START_ENCRYPTION_REQ { EnRand }
    Note over B: SK = Es(E3(LK, EnRand, ACO), KeySize)
    B->>A: ENC( LMP_ACCEPTED, SK )
    Note over A: Verify ENC( LMP_ACCEPTED, SK )
```

## Facts & Rules

### R_0: [] => S_0

```mermaid
sequenceDiagram
    participant A as Alice ( Central )
    participant B as Bob ( Peripheral )
 
 Note over A: AddressA: Alice 的地址
 Note over B: AddressB: Bob 的地址
    Note over A,B: Alice and Bob shared the LK
```

* **Rule Name:** `InitDevices`
* **Facts In**
* **Facts  Out**
  * **S_0:** `!PairedDevices($A, $B, ~LK)`
* **Only Once**

### R_A1: S_0=> S_A1

```mermaid
sequenceDiagram
    participant A as Alice ( Central )
    participant B as Bob ( Peripheral )

    Note over A: Fresh AuRand <br/> SRES, ACO = E1(LK, AuRand, AddressB)
    A->>B: LMP_AU_RAND { AuRand }
```

* **Rule Name:** `CenSendAuRand`
* **Facts In**
  * **S_0:** `!PairedDevices($A, $B, LK)`
* **Facts  Out**
  * **Out:** `Out($A, $B, 'AU_RAND', AuRand)`
  * **S_A1:** `State_CenSendAuRand($A, $B, LK, SRES, ACO)`
  
### R_B1: S_0 => S_B1

```mermaid
sequenceDiagram
    participant A as Alice ( Central )
    participant B as Bob ( Peripheral )
 
    A->>B: LMP_AU_RAND { AuRand }
    Note over B: SRES, ACO = E1(LK, AuRand, AddressB)
    B->>A: LMP_SRES { SRES }
```

* **Rule Name:** `PerRecvAuRand`
* **Facts In**
  * **In:** `In($A, $B, 'AU_RAND', AuRand)`
  * **S_0:** `!PairedDevices($A, $B, LK)`

* **Facts Out**
  * **Out:** `Out($B, $A, 'SERS', SERS)`
  * **S_B1：** `State_PerRecvAuRand($B, $A, LK, ACO)`

### R_A2: S_A1 => S_A2

```mermaid
sequenceDiagram
    participant A as Alice ( Central )
    participant B as Bob ( Peripheral )

    B->>A: LMP_SRES { SRES }
    Note over A: Verify SRES
    A->>B: LMP_ENCRYPTION_KEY_SIZE_REQ { KeySize }
```

* **Rule Name:** `CenNegotiateKeysize`
* **Facts In**
  * **In:** `In($B, $A, 'SERS', SERS_B)`
  * **S_A1:** `State_CenSendAuRand($A, $B, LK, SRES, ACO)`
* **Facts Out**
  * **Out:** `Out($A, $B, 'KEYSIZE', '16')`
  * **S_A2:** `State_CenNegotiateKeysize($A, $B, LK, ACO, '16')`

### R_B2: S_B1 => S_B2

```mermaid
sequenceDiagram
    participant A as Alice ( Central )
    participant B as Bob ( Peripheral )

    A->>B: LMP_ENCRYPTION_KEY_SIZE_REQ { KeySize }
    B->>A: LMP_ACCEPTED
```

* **Rule Name:** `PerNegotiateKeysize`
* **Facts In**
  * **In:** `In($A, $B, 'KEYSIZE', keysize)`
  * **S_B1:** `State_PerRecvAuRand($B, $A, LK, ACO)`
* **Facts Out**
  * **Out:** `Out($B, $A, 'ACCEPTED')`
  * **S_B2:** `State_PerNegotiateAccept($B, $A, LK, ACO, keysize)`

### R_A3: S_A2 => S_A3

```mermaid
sequenceDiagram
    participant A as Alice ( Central )
    participant B as Bob ( Peripheral )

    B->>A: LMP_ACCEPTED
    Note over A: Fresh EnRand <br/> SK = Es(E3(LK, EnRand, ACO), KeySize)
    A->>B: LMP_START_ENCRYPTION_REQ { EnRand }
```

* **Rule Name:** `CenStartEnc`
* **Facts In**
  * **In:** `In($B, $A, 'ACCEPTED')`
  * **S_A2 :** `State_CenNegotiateKeysize($A, $B, LK, ACO, keysize)`
* **Facts Out**
  * **Out:** `Out($A, $B, 'EN_RAND', EnRand)`
  * **S_A2:** `State_CenStartEnc($A, $B, LK, ACO, keysize, SK)`

### R_B3: S_B2 => S_B3

```mermaid
sequenceDiagram
    participant A as Alice ( Central )
    participant B as Bob ( Peripheral )

    A->>B: LMP_START_ENCRYPTION_REQ { EnRand }
    Note over B: SK = Es(E3(LK, EnRand, ACO), KeySize)
    B->>A: ENC( LMP_ACCEPTED, SK )
```

* **Rule Name:** `PerStartEnc`
* **Facts In**
  * **In:** `In($A, $B, 'EN_RAND', EnRand)`
  * **S_B2:** `State_PerNegotiateAccept($B, $A, LK, ACO, keysize)`
* **Facts Out**
  * **Out:** `Out($B, $A, 'ENC_ACCEPTED', senc('ACCEPTED', SK))`
  * **S_B3:** `State_PerNegotiateAccept($B, $A, LK, ACO, keysize, SK)`

### R_A4: S_A3 => S_A4

```mermaid
sequenceDiagram
    participant A as Alice ( Central )
    participant B as Bob ( Peripheral )

    B->>A: ENC( LMP_ACCEPTED, SK )
    Note over A: Verify ENC( LMP_ACCEPTED, SK )
```

* **Rule Name:** `CentSessionEstablished`
* **Facts In**
  * **In:** `In($B, $A, 'ENC_ACCEPTED', senc('ACCEPTED', SK))`
  * **S_A3 :** `State_CenStartEnc($A, $B, LK, ACO, keysize, SK)`
* **Facts Out**
