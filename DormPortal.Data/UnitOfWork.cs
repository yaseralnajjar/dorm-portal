﻿using System;
using DormPortal.Core.Models;
using Microsoft.EntityFrameworkCore;

namespace DormPortal.Data
{
	public class UnitOfWork : IUnitOfWork
	{
		private DormitoryRespository _dormitoryRespository;
		private RoomRespository _roomRespository;
		private StudentRepository _studentRepository;
		private readonly DormPortalDbContext _context;

		public UnitOfWork(DormPortalDbContext context)
		{
			_context = context;
		}

		public TRepository LazyGenericRepository<TRepository, TEntity>
			(ref TRepository genericRepository, DbSet<TEntity> dbSet)
			where TRepository: GenericRepository<TEntity>
			where TEntity : BaseEntity
		{
			genericRepository = genericRepository ??
								(TRepository)Activator.CreateInstance(typeof(TRepository), dbSet);

			//var test = genericRepository as StudentRepository;

			return genericRepository;
		}

		public DormitoryRespository DormitoryRespository =>
			LazyGenericRepository<DormitoryRespository, Dormitory>(ref _dormitoryRespository, _context.Dormitories);

		public RoomRespository RoomRespository =>
			LazyGenericRepository<RoomRespository, Room>(ref _roomRespository, _context.Rooms);


		public StudentRepository StudentRepository =>
			LazyGenericRepository<StudentRepository, Student>(ref _studentRepository, _context.Students);

		public int Commit()
		{
			return _context.SaveChanges();
		}
	}
}