import { Entity, PrimaryGeneratedColumn, Column, OneToMany } from 'typeorm';
import { SellTransaction } from './SellTransaction.entity';
import { BuyTransaction } from './BuyTransaction.entity';

@Entity()
export default class Round {
    @PrimaryGeneratedColumn('uuid')
    id: string;

    @Column()
    startDate: Date;

    @Column()
    endDate: Date;

    @Column('float', {
        nullable: true,
    })
    mti: number;

    @Column('float', {
        nullable: true,
    })
    marketPrice: number;

    @Column({
        default: true,
    })
    isActive: boolean;

    @OneToMany(_ => SellTransaction, sellerTransaction => sellerTransaction.round)
    sellTransactions: SellTransaction[];

    @OneToMany(_ => BuyTransaction, buyerTransaction => buyerTransaction.round)
    buyTransactions: BuyTransaction[];
}
